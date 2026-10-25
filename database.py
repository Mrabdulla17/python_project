import sqlite3
from datetime import datetime


# Create database and table
def create_database():
    connection = None

    try:
        connection = sqlite3.connect("bmi_records.db")
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)

        connection.commit()
        return True

    except sqlite3.Error as e:
        print(f"Database error while creating database: {e}")
        return False

    finally:
        if connection:
            connection.close()


# Save BMI record
def save_record(name, weight, height, bmi, category):
    connection = None

    try:
        connection = sqlite3.connect("bmi_records.db")
        cursor = connection.cursor()

        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO bmi_records
            (name, weight, height, bmi, category, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            weight,
            height,
            bmi,
            category,
            current_date
        ))

        connection.commit()
        return True

    except sqlite3.Error as e:
        print(f"Database error while saving record: {e}")
        return False

    finally:
        if connection:
            connection.close()


# Get all BMI records
def get_records():
    connection = None

    try:
        connection = sqlite3.connect("bmi_records.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, name, weight, height, bmi, category, date
            FROM bmi_records
            ORDER BY id DESC
        """)

        records = cursor.fetchall()

        return records

    except sqlite3.Error as e:
        print(f"Database error while reading records: {e}")
        return []

    finally:
        if connection:
            connection.close()


# Delete BMI record
def delete_record(record_id):
    connection = None

    try:
        connection = sqlite3.connect("bmi_records.db")
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM bmi_records WHERE id = ?",
            (record_id,)
        )

        connection.commit()
        return True

    except sqlite3.Error as e:
        print(f"Database error while deleting record: {e}")
        return False

    finally:
        if connection:
            connection.close()


# Run this file directly to create the database
if __name__ == "__main__":
    if create_database():
        print("Database created successfully!")
    else:
        print("Failed to create database.")

