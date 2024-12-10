import sqlite3

def Insert_data(cursor, conn, table_name, data):
        """Insert data into a table."""
        try:
            placeholders = ", ".join("?" * len(data))
            insert_query = f"INSERT INTO {table_name} VALUES ({placeholders});"
            cursor.execute(insert_query, data)
            conn.commit()
            print("\nData inserted successfully.")
            return {
                 "status": "success",
                 "message": "\nData inserted successfully."
            }
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")
            return {
                 "status": "fail",
                 "message": "\bError inserting data."
            }