# publichost
**Make localhost public**  

Share your local web apps instantly with a public URL.  

🔗 **Visit [publichost.dev](https://publichost.dev)**

---

## 🚀 Installation
```sh
pip install publichost
```

---

## 🏁 Quick Start

Expose **any web server** in **one line**.

```python
from publichost import Tunnel
tunnel = Tunnel(port=3000)  # Expose local port 3000

print(f"🔗 {tunnel.public_url}")  # Get your public link
```

**Example Output:**
```
🔗 https://x8k2p.publichost.dev
```
Your local app is now **online and shareable**.

---

## 🌍 Works with Any Python Web Framework

### Flask
```python
from flask import Flask
from publichost import Tunnel

app = Flask(__name__)
tunnel = Tunnel(port=5000)

@app.route("/")
def home():
    return "Hello, publichost!"

if __name__ == "__main__":
    print(f"🔗 {tunnel.public_url}")
    app.run(port=5000)
```

### FastAPI
```python
from fastapi import FastAPI
from publichost import Tunnel
import uvicorn

app = FastAPI()
tunnel = Tunnel(port=8000)

@app.get("/")
async def read_root():
    return {"message": "Hello, publichost!"}

if __name__ == "__main__":
    print(f"🔗 {tunnel.public_url}")
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

**Works with any Python web server**, including **Django, Quart, Starlette, and more**.

---

## 🔧 Custom Subdomains
By default, publichost assigns a **random subdomain** like `x8k2x.publichost.dev`.  
To set a **custom subdomain**, pass it as an argument:

```python
tunnel = Tunnel(port=5000, subdomain="mycustomapp")
```
Your app will be available at **`https://mycustomapp.publichost.dev`**.

**Subdomain Rules:**
- Must be **6-32 characters**
- Can contain **letters, numbers, and hyphens**
- Cannot be a **reserved system word** (e.g., `admin`, `www`, `api`)

---

## 📚 How It Works
1. Install `publichost`
2. Add **one line of code**
3. Get a **public URL** instantly

For more details, visit **[publichost.dev](https://publichost.dev)**.
