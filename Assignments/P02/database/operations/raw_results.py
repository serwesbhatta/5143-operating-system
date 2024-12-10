def Raw_results(results):
    """
    Convert raw results to a list of table names.
    
    Args:
        results: The raw database results from the SQLite query.
    
    Returns:
        List: A list of table names.
    """
    return [row[0] for row in results]
