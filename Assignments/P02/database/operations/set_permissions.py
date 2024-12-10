import sqlite3

def Set_permissions(cursor, conn, table_name, permissions, filters):
    query = f"""
            UPDATE {table_name}
            SET 
                read_permission = ?, 
                write_permission = ?, 
                execute_permission = ?,
                world_read = ?, 
                world_write = ?, 
                world_execute = ?
            WHERE 
                oid = ? AND 
                pid = ? AND 
                name = ?;
        """
    name = filters["name"]
    values = [
        permissions["owner_read"],
        permissions["owner_write"],
        permissions["owner_execute"],
        permissions["world_read"],
        permissions["world_write"],
        permissions["world_execute"],
        filters["oid"],
        filters["pid"],
        name,
    ]

    try:
        cursor.execute(query, values)
        conn.commit()

        return {
            "status": "success",
            "message": f"Permissions successfully updated for {name} in {table_name}."
        }
    except sqlite3.Error as e:
        return {
            "status": "fail",
            "message": f"\nError updating permissions: {str(e)}"
        }
