import sqlite3
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password_hash TEXT)''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def add_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
              (username, hash_password(password)))
    conn.commit()
    conn.close()

@app.route('/validate', methods=['POST'])
def validate():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    if result and result[0] == hash_password(password):
        return jsonify({"valid": True, "message": "Usuario autenticado"})
    return jsonify({"valid": False, "message": "Credenciales inválidas"})

if __name__ == '__main__':
    init_db()
    # Agregar a los integrantes (reemplaza con nombres reales)
    add_user("Kevin", "pass123")
    add_user("Jhan", "pass456")
    add_user("Valdes", "pass789")
    add_user("Bernilla", "pass963")
    app.run(host='0.0.0.0', port=5800)