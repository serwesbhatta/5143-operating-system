import sqlite3

def Update_data(cursor, conn, table_name, column, new_value, condition_column, condition_value):
        """Update data in a table based on a condition."""
        try:
            update_query = f"UPDATE {table_name} SET {column} = ? WHERE {condition_column} = ?;"
            cursor.execute(update_query, (new_value, condition_value))
            conn.commit()
            # print("Data updated successfully.")
            return {"success": True, "message": "Data updated successfully."}
        except sqlite3.Error as e:
            return {"success": False, "message": f"Error updating data: {e}"}