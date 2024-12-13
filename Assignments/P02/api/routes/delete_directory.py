from fastapi import HTTPException
from database.sqliteCRUD import SqliteCRUD

def Delete_directory(fsDB: SqliteCRUD, oid: int, pid: int, name: str):
    """
    Delete a directory and its contents from the simulated filesystem (database) and log the action.
    :param directory_name: The name of the directory to be deleted.
    """
    if fsDB:
        # Check if the directory exists in the database
        filters = {"oid": oid, "name": name, "pid": pid}  # Assuming root directory
        directory_record = fsDB.read_data("directories", filters)
        
        if directory_record:
            # Delete the directory from the database
            fsDB.delete_data("directories", "name", name)
            return {"status": "success", "message": f"Directory '{name}' deleted from the database."}
        else:
            return {"status": "fail", "message": f"Directory '{name}' not found in the database."}
    else:
        return {"status": "fail", "message": "Database connection not found."}