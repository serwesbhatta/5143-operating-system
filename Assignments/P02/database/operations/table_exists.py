import sqlite3

def Table_exists(cursor, table_name):
        """Check if a table exists."""
        try:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
            return cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False