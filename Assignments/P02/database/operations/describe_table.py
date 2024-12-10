from .formatted_results import Formatted_results

def Describe_table(cursor, table_name, raw=False):
        """Describe the structure of a table."""
        cursor.execute(f"PRAGMA table_info({table_name});")
        results = cursor.fetchall()
        if raw:
            return [{ "column_name": row[1], "data_type": row[2], "isnull": "NULL" if row[3] == 0 else "NOT NULL" } for row in results]
        return Formatted_results(results)