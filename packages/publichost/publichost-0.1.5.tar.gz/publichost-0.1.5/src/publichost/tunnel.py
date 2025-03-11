# src/publichost/tunnel.py
import asyncio
import json
import logging
import re
import aiohttp
import websockets
import threading
import time
import os
import socket
from typing import Optional
from .exceptions import ConnectionError, TunnelError
from .utils import generate_subdomain, RESERVED_WORDS

logger = logging.getLogger('publichost.tunnel')

class Tunnel:
    """A tunnel that makes a local port accessible via a public URL.

    Usage:
        ```python
        from flask import Flask
        from publichost import Tunnel

        app = Flask(__name__)
        tunnel = Tunnel(port=5000)

        @app.route("/")
        def hello():
            return "Hello World!"
        ```
    """
    
    MIN_SUBDOMAIN_LENGTH = 6
    MAX_SUBDOMAIN_LENGTH = 32
    SUBDOMAIN_PATTERN = re.compile(r'^[a-z0-9][a-z0-9-]{4,30}[a-z0-9]$')
    
    def __init__(
        self, 
        port: int, 
        subdomain: Optional[str] = None,
        dev_mode: bool = False
    ) -> None:
        """Create a tunnel to expose a local port.

        Args:
            port: Local port to tunnel
            subdomain: Optional custom subdomain (auto-generated if not provided)
            dev_mode: Enable development mode (uses localhost)
        """
        # Basic setup
        self.port = port
        self.subdomain = self._validate_subdomain(subdomain) if subdomain else self._generate_subdomain()
        self.ws_url = self._get_ws_url(dev_mode)
        self.public_url = self._get_public_url(dev_mode)

        # Initialize connection handling
        self._shutdown = threading.Event()
        self._connected = threading.Event()
        self._server_ready = threading.Event()

        # Start tunnel with server monitoring
        self._start_monitor()
        self._start_tunnel()
        
        # Print tunnel URL in a server-like format
        print(f" * Tunnel URL: {self.public_url}")

    def _check_server(self) -> bool:
        """Check if local server is responding."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect(('localhost', self.port))
                return True
        except:
            return False

    def _start_monitor(self) -> None:
        """Start monitoring local server availability."""
        def monitor():
            while not self._shutdown.is_set():
                self._server_ready.set() if self._check_server() else self._server_ready.clear()
                time.sleep(1)
        
        threading.Thread(target=monitor, daemon=True).start()

    def _validate_subdomain(self, subdomain: str) -> str:
        """Validate and normalize a custom subdomain."""
        if not isinstance(subdomain, str):
            raise TunnelError("Subdomain must be a string")
        
        subdomain = subdomain.lower().strip()
        
        if len(subdomain) < self.MIN_SUBDOMAIN_LENGTH:
            raise TunnelError(f"Subdomain must be at least {self.MIN_SUBDOMAIN_LENGTH} characters")
        
        if len(subdomain) > self.MAX_SUBDOMAIN_LENGTH:
            raise TunnelError(f"Subdomain must be at most {self.MAX_SUBDOMAIN_LENGTH} characters")
        
        if not self.SUBDOMAIN_PATTERN.match(subdomain):
            raise TunnelError("Subdomain can only contain letters, numbers, and hyphens")
        
        if subdomain in RESERVED_WORDS:
            raise TunnelError(f"'{subdomain}' is a reserved subdomain")
        
        return subdomain

    def _generate_subdomain(self) -> str:
        """Generate a valid subdomain."""
        return generate_subdomain()

    def _get_ws_url(self, dev_mode: bool) -> str:
        """Get WebSocket URL."""
        if dev_mode:
            return f"ws://localhost:{self.port}/ws"
        return os.getenv("PUBLICHOST_WS_URL", "wss://tunnel.publichost.dev/ws")

    def _get_public_url(self, dev_mode: bool) -> str:
        """Get public URL."""
        domain = f"localhost:{self.port}" if dev_mode else os.getenv("PUBLICHOST_DOMAIN", "publichost.dev")
        protocol = "http" if dev_mode else "https"
        return f"{protocol}://{self.subdomain}.{domain}"

    def _start_tunnel(self) -> None:
        """Start tunnel in background thread."""
        def run():
            while not self._shutdown.is_set():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(self._maintain_connection())
                except Exception as e:
                    if not self._shutdown.is_set():
                        time.sleep(1)
                finally:
                    loop.close()

        threading.Thread(target=run, daemon=True).start()

    async def _maintain_connection(self) -> None:
        """Maintain WebSocket connection."""
        async with websockets.connect(
            self.ws_url,
            ping_interval=15,
            ping_timeout=10
        ) as ws:
            await ws.send(json.dumps({
                "type": "register",
                "tunnel_id": self.subdomain,
                "local_port": self.port
            }))
            
            self._connected.set()
            
            await asyncio.gather(
                self._handle_messages(ws),
                self._keep_alive(ws)
            )

    async def _keep_alive(self, ws: websockets.WebSocketClientProtocol) -> None:
        """Send periodic heartbeats."""
        while True:
            try:
                await asyncio.sleep(15)
                if self._server_ready.is_set():
                    await ws.send(json.dumps({"type": "ping"}))
            except:
                break

    async def _handle_messages(self, ws: websockets.WebSocketClientProtocol) -> None:
        """Handle incoming messages."""
        async for message in ws:
            if not self._server_ready.is_set():
                # Server not ready, return error
                data = json.loads(message)
                await ws.send(json.dumps({
                    "type": "response",
                    "request_id": data.get("request_id"),
                    "status": 502,
                    "headers": {},
                    "content": "Local server not ready"
                }))
                continue
            
            try:
                data = json.loads(message)
                if data["type"] == "request":
                    response = await self._handle_request(data)
                    await ws.send(json.dumps(response))
            except Exception as e:
                logger.error(f"Error handling message: {e}")

    async def _handle_request(self, data: dict) -> dict:
        """Handle proxied request."""
        url = f"http://localhost:{self.port}{data.get('path', '/')}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=data["method"],
                    url=url,
                    headers=data["headers"],
                    data=data.get("body", ""),
                    timeout=aiohttp.ClientTimeout(total=30),
                    allow_redirects=False
                ) as response:
                    return {
                        "type": "response",
                        "request_id": data["request_id"],
                        "status": response.status,
                        "headers": dict(response.headers),
                        "content": await response.text()
                    }
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return {
                "type": "response",
                "request_id": data["request_id"],
                "status": 502,
                "headers": {},
                "content": "Failed to reach local server"
            }

    def close(self) -> None:
        """Close the tunnel."""
        self._shutdown.set()

    def __enter__(self) -> 'Tunnel':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def __str__(self) -> str:
        return self.public_url