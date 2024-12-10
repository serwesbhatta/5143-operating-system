import sqlite3

def Set_file_permissions_db(cursor, conn, table_name, mode, filters):
  if filters is None or not all(key in filters for key in ['name', 'oid', 'pid']):
        return False

  # Constructing the SQL WHERE clause based on filters
  conditions = [f"{key} = ?" for key in filters]
  where_clause = " AND ".join(conditions)
  values = list(filters.values())

  # Add the new permissions to the values list which will be passed to execute()
  values.append(mode)

  # Construct SQL update statement
  sql = f"UPDATE {table_name} SET permissions = ? WHERE {where_clause}"

  try:
      # Execute the update statement
      cursor.execute(sql, values)
      conn.commit()  # Committing changes to the database
      return True
  except sqlite3.Error as e:
      print(f"Database error: {e}")
      return False
  