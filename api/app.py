from flask import Flask, request
import hashlib
import subprocess
import os

app = Flask(__name__)


ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "default_secure_value_change_me")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/login")
def login():
    username = request.args.get("username")
    password = request.args.get("password")

    if not username or not password:
        return "Missing credentials", 400

    if username == "admin" and hash_password(password) == hash_password(ADMIN_PASSWORD):
        return "Logged in"
    return "Invalid credentials", 401

@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")
    result = subprocess.check_output(
        f"ping -c 1 {host}",
        shell=True
    )
    return result
@app.route("/hello")
def hello():
    name = request.args.get("name", "user")
    
    return f"<h1>Hello {name}</h1>"


if __name__ == "__main__":
    
    app.run(debug=True)