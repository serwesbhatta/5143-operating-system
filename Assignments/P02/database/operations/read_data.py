import sqlite3

def Read_data(cursor, table_name, filters=None):
        """
        Read data from a table, with optional filtering.
    
        Args:
            table_name (str): The name of the table to query.
            filters (dict, optional): A dictionary of filters to apply to the query (e.g., {"name": "filename"}).
                                    If None, all rows will be returned.

        Returns:
            list: The query results as a list of rows, or an empty list if no results.
        """
        try:
            select_query = f"SELECT * FROM {table_name}"

             # If filters are provided, add a WHERE clause
            if filters:
                conditions = [f"{key} = ?" for key in filters.keys()]
                where_clause = " WHERE " + " AND ".join(conditions)
                select_query += where_clause

            cursor.execute(select_query, tuple(filters.values()) if filters else ())
            results = cursor.fetchall()

            if results:
                return results
            else:
                return []
        except sqlite3.Error as e:
            print(f"Error reading data: {e}")