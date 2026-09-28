from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)


def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "notesdb"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres")
    )


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api/notes", methods=["GET"])
def get_notes():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, title, content FROM notes")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    notes = [{"id": r[0], "title": r[1], "content": r[2]} for r in rows]
    return jsonify(notes), 200


@app.route("/api/notes", methods=["POST"])
def create_note():
    data = request.get_json() or {}

    title = data.get("title")
    if not title:
        return jsonify({"error": "El título es obligatorio"}), 400

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO notes (title, content) VALUES (%s, %s) RETURNING id",
        (title, data.get("content", ""))
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": new_id, "title": title, "content": data.get("content", "")}), 201


@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM notes WHERE id = %s", (note_id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Nota eliminada"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
