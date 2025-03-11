import string
import random
import re

RESERVED_WORDS = {
    # System and admin paths
    'admin', 'administrator', 'root', 'system', 'dashboard', 'console',
    'api', 'auth', 'login', 'dev', 'test', 'staging', 'prod', 'production',
    'internal', 'app', 'host', 'server', 'database', 'db', 'mail', 'smtp',
    'ftp', 'ssh', 'dns', 'mx', 'ns', 'ns1', 'ns2', 'web', 'www', 'control',
    
    # Common service names
    'grafana', 'prometheus', 'kibana', 'jenkins', 'gitlab', 'github', 
    'bitbucket', 'jira', 'confluence', 'wiki', 'docs', 'registry',
    
    # Security related
    'security', 'secure', 'ssl', 'tls', 'vpn', 'firewall', 'proxy',
    'sysadmin', 'webmaster', 'postmaster', 'hostmaster',
    
    # Common subdomains
    'blog', 'shop', 'store', 'support', 'help', 'status', 'metrics',
    'monitor', 'stats', 'analytics', 'cdn', 'assets', 'static', 'media',
    
    # Special terms
    'localhost', 'publichost', 'example', 'test', 'invalid', 'undefined', 'null'
}

SUBDOMAIN_PATTERN = re.compile(r'^[a-z0-9][a-z0-9-]{4,30}[a-z0-9]$')

def generate_subdomain() -> str:
    """
    Generate a random subdomain that follows the `app-[6 char]` pattern.

    Returns:
        str: A safe random subdomain like 'app-x8k2p9'
    """
    chars = string.ascii_lowercase + string.digits
    while True:
        subdomain = f"app-{''.join(random.choices(chars, k=6))}"
        if subdomain not in RESERVED_WORDS:
            return subdomain  # Ensure it's not a reserved word

def validate_subdomain(subdomain: str) -> str:
    """
    Validate a custom subdomain.

    Args:
        subdomain (str): The subdomain to validate.

    Returns:
        str: The validated subdomain.

    Raises:
        ValueError: If the subdomain is invalid.
    """
    if not isinstance(subdomain, str):
        raise ValueError("Subdomain must be a string")

    subdomain = subdomain.lower().strip()

    if len(subdomain) < 6 or len(subdomain) > 32:
        raise ValueError("Subdomain length must be between 6-32 characters")

    if not SUBDOMAIN_PATTERN.match(subdomain):
        raise ValueError("Subdomain can only contain letters, numbers, and hyphens")

    if subdomain in RESERVED_WORDS:
        raise ValueError(f"'{subdomain}' is a reserved subdomain")

    return subdomain
