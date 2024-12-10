import sqlite3

def Drop_table(cursor, conn, table_name):
        """Drop a table by name."""
        try:
            drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
            cursor.execute(drop_table_query)
            conn.commit()
            print(f"Dropped table '{table_name}' successfully.")
        except sqlite3.Error as e:
            print(f"Error dropping table: {e}")