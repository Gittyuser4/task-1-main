from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import time
import psycopg2
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# ---------- DB CONFIG ----------
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT", "5432")


def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT"),
            )
            conn.close()
            print("Database is ready")
            break
        except psycopg2.OperationalError:
            print("Waiting for database...")
            time.sleep(2)




def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=int(DB_PORT),
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def init_db():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
    )
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

# ---------- UI ROUTE ----------
@app.route("/")
def index():
    return render_template("auth.html")

# ---------- REGISTER ----------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM users WHERE username=%s", (username,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({"success": False, "message": "User already exists"})

    hashed_password = generate_password_hash(password, method="scrypt")
    cur.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, hashed_password)
    )
    conn.commit()

    cur.close()
    conn.close()
    return jsonify({"success": True, "message": "Registration successful"})

# ---------- LOGIN ----------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT password FROM users WHERE username=%s", (username,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return jsonify({"success": False, "message": "User not found"})

    if check_password_hash(row[0], password):
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"})

# ---------- RUN ----------
if __name__ == "__main__":
    wait_for_db()
    init_db()
    app.run(host="0.0.0.0", port=5000)
