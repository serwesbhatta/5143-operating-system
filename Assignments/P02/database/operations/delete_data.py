import sqlite3

def Delete_data(cursor, conn, table_name, condition_column, condition_value):
        """Delete data from a table based on a condition."""
        try:
            delete_query = f"DELETE FROM {table_name} WHERE {condition_column} = ?;"
            cursor.execute(delete_query, (condition_value,))
            conn.commit()
           
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")