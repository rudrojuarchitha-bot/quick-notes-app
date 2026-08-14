from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "notes.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/notes", methods=["GET"])
def get_notes():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT id, content FROM notes ORDER BY id DESC")
    notes = cursor.fetchall()

    conn.close()

    return jsonify([
        {"id": note[0], "content": note[1]}
        for note in notes
    ])


@app.route("/notes", methods=["POST"])
def add_note():
    data = request.get_json()

    content = data.get("content", "").strip()

    if not content:
        return jsonify({"error": "Note cannot be empty"}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notes (content) VALUES (?)",
        (content,)
    )

    note_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({
        "id": note_id,
        "content": content
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True)