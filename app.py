from flask import Flask, render_template, request, jsonify
import sqlite3
from database import create_database

create_database()
app = Flask(__name__)

DATABASE_NAME = "library.db"


def search_books(keyword):
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM books
        WHERE title LIKE ?
        OR author LIKE ?
        OR subject LIKE ?
        OR keywords LIKE ?
    """, (
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    books = [dict(row) for row in cursor.fetchall()]
    connection.close()

    return books


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    keyword = data.get("keyword", "").strip()

    if not keyword:
        return jsonify([])

    results = search_books(keyword)
    return jsonify(results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)