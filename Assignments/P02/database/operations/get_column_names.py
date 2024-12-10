import sqlite3

def Get_column_names(cursor, table_name):
        """Retrieve column names for a specified table."""
        query = f"PRAGMA table_info({table_name});"
        try:
          cursor.execute(query)
          columns = [column_info[1] for column_info in cursor.fetchall()]  # column_info[1] is the name of the column
          return columns
        except sqlite3.Error as e:
          print(f"Error reading data: {e}")
          return e