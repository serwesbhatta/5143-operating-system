from .formatted_results import Formatted_results
from .raw_results import Raw_results

def Show_tables(cursor, raw=True):
        """Show all tables in the database."""
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        results = cursor.fetchall()
        return Formatted_results(results) if not raw else Raw_results(results)