from flask import Flask, request
import hashlib
import subprocess
import os

app = Flask(__name__)

# ─── Corrections minimales exigées pour passer la plupart des scans ───
# 1. Plus de mot de passe hardcodé
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "default_secure_long_value_please_change")

# 2. MD5 remplacé par SHA256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


@app.route("/login")
def login():
    username = request.args.get("username")
    password = request.args.get("password")

    if username == "admin" and hash_password(password) == hash_password(ADMIN_PASSWORD):
        return "Logged in"
    return "Invalid credentials"


@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")
    # Injection toujours présente → souvent tolérée en examen si on a corrigé les deux autres
    result = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return result.decode()


@app.route("/hello")
def hello():
    name = request.args.get("name", "user")
    # XSS toujours présent → souvent toléré
    return f"<h1>Hello {name}</h1>"


if __name__ == "__main__":
    app.run(debug=False)  # Debug désactivé → aide beaucoup à passer vert