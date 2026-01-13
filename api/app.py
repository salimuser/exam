from flask import Flask, request, jsonify
import sqlite3
import bcrypt
import os

app = Flask(__name__)

DATABASE = "users.db"

def get_db():
    return sqlite3.connect(DATABASE)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Invalid input"}), 400

    conn = get_db()
    cursor = conn.cursor()

  
    cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )

    row = cursor.fetchone()
    conn.close()

    if row and bcrypt.checkpw(password.encode(), row[0]):
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 401


@app.route("/hash", methods=["POST"])
def hash_password():
    data = request.get_json()
    pwd = data.get("password")

    if not pwd:
        return jsonify({"error": "Password required"}), 400

 
    hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())
    return jsonify({"hash": hashed.decode()})


@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Secure DevSecOps API"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
