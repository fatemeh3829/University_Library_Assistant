
import sqlite3

DATABASE_NAME = "library.db"


def create_database():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            publisher TEXT,
            publish_year INTEGER,
            subject TEXT,
            keywords TEXT
        )
    """)

    sample_books = [
        (
            "مبانی برنامه نویسی پایتون",
            "محمد رضایی",
            "انتشارات دانشگاهی",
            1402,
            "برنامه نویسی",
            "پایتون برنامه نویسی Python"
        ),
        (
            "هوش مصنوعی",
            "استوارت راسل",
            "انتشارات علم",
            1401,
            "هوش مصنوعی",
            "AI Artificial Intelligence یادگیری ماشین"
        ),
        (
            "پایگاه داده ها",
            "علی احمدی",
            "انتشارات فناوری",
            1400,
            "پایگاه داده",
            "SQL دیتابیس بانک اطلاعاتی"
        ),
        (
            "مهندسی نرم افزار",
            "راجر پرسمن",
            "انتشارات دانشگاهی",
            1399,
            "مهندسی نرم افزار",
            "Software Engineering طراحی نرم افزار"
        ),
        (
            "شبکه های کامپیوتری",
            "اندرو تننباوم",
            "انتشارات فناوری",
            1402,
            "شبکه",
            "شبکه کامپیوتر اینترنت"
        )
    ]

    cursor.executemany("""
        INSERT INTO books
        (title, author, publisher, publish_year, subject, keywords)
        SELECT ?, ?, ?, ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM books
            WHERE title = ? AND author = ?
        )
    """, [
        book + (book[0], book[1])
        for book in sample_books
    ])

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    print("Database created successfully!")
