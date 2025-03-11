from flask import Flask
from publichost import Tunnel

app = Flask(__name__)
tunnel = Tunnel(port=5000)
print ("Launching tunnel")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"