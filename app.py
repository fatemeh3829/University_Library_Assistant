
from flask import Flask, render_template, request, jsonify
import sqlite3
from database import create_database

create_database()

app = Flask(__name__)

DATABASE_NAME = "library.db"


def search_books(keyword, language="all", search_type="all"):
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    fields = {
        "book": ["b.title"],
        "author": ["b.author"],
        "subject": ["b.subject", "b.keywords"],
        "all": [
            "b.title", "b.author", "b.subject", "b.keywords",
            "related.title", "related.author",
            "related.subject", "related.keywords"
        ]
    }

    selected_fields = fields.get(search_type, fields["all"])

    conditions = " OR ".join(
        f"{field} LIKE ?" for field in selected_fields
    )

    query = f"""
        SELECT DISTINCT b.*
        FROM books b
        LEFT JOIN books related
        ON (
            related.original_book_id = b.id
            OR b.original_book_id = related.id
        )
        WHERE ({conditions})
    """

    params = [f"%{keyword}%"] * len(selected_fields)

    if language == "fa":
        query += " AND b.language = ?"
        params.append("Persian")
    elif language == "en":
        query += " AND b.language = ?"
        params.append("English")

    cursor.execute(query, params)
    books = [dict(row) for row in cursor.fetchall()]
    connection.close()

    return books


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    data = request.get_json() or {}

    keyword = data.get("keyword", "").strip()
    language = data.get("language", "all")
    search_type = data.get("search_type", "all")

    if language not in ["all", "fa", "en"]:
        language = "all"

    if search_type not in ["all", "book", "author", "subject"]:
        search_type = "all"

    if not keyword:
        return jsonify([])

    results = search_books(keyword, language, search_type)

    return jsonify(results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
