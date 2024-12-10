import sqlite3

def Create_table(cursor, conn, table_name, columns):
        """Create a new table with specified columns."""
        try:
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
            cursor.execute(create_table_query)
            conn.commit()
            print(f"Table '{table_name}' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")