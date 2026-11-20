
import sqlite3

DATABASE_NAME = "library.db"


def create_database():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # ایجاد جدول کتاب‌ها
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            publisher TEXT,
            publish_year INTEGER,
            subject TEXT,
            keywords TEXT,
            isbn TEXT,
            source_url TEXT,
            language TEXT,
            original_book_id INTEGER,
            edition_type TEXT
        )
    """)

    # بررسی ستون‌های موجود
    cursor.execute("PRAGMA table_info(books)")
    existing_columns = [
        column[1] for column in cursor.fetchall()
    ]

    # اضافه کردن ستون‌های جدید به جدول قدیمی
    new_columns = {
        "isbn": "TEXT",
        "source_url": "TEXT",
        "language": "TEXT",
        "original_book_id": "INTEGER",
        "edition_type": "TEXT"
    }

    for column_name, column_type in new_columns.items():
        if column_name not in existing_columns:
            cursor.execute(
                f"ALTER TABLE books ADD COLUMN {column_name} {column_type}"
            )

    # جلوگیری از ثبت ISBN تکراری
    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_books_isbn
        ON books(isbn)
        WHERE isbn IS NOT NULL AND isbn != ''
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    print("Database updated successfully!")
