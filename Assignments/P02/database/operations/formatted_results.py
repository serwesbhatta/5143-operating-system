from prettytable import PrettyTable

def Formatted_results(results):
    """Format results using PrettyTable."""
    table = PrettyTable()
    table.field_names = ["Column ID", "Name", "Type", "Not Null", "Default", "Primary Key"]
    table.add_rows(results)
    return table