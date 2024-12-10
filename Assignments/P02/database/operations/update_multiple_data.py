def Update_multiple_data(
    cursor, conn, table_name: str, filters: dict, new_values: dict
):
    """
    Updates data in a table based on multiple conditions and new values.

    Args:
        table_name (str): The name of the table.
        filters (dict): A dictionary of column-value pairs for the WHERE clause.
        new_values (dict): A dictionary of column-value pairs to update.

    Returns:
        dict: Success or error message.
    """
    if not filters or not new_values:
        return {"success": False, "message": "Filters and new_values cannot be empty."}

    # Create SET clause dynamically from new_values
    set_clause = ", ".join([f"{key} = ?" for key in new_values.keys()])

    # Create WHERE clause dynamically from filters
    where_clause = " AND ".join([f"{key} = ?" for key in filters.keys()])

    query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

    try:
        cursor.execute(query, (*new_values.values(), *filters.values()))
        conn.commit()

        return {"success": True, "message": "Update successful."}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
