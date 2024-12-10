from fastapi import HTTPException
from database.sqliteCRUD import SqliteCRUD

def Delete_directory(fsDB: SqliteCRUD, oid: int, pid: int, directory_name: str):
    """
    Delete a directory and its contents from the simulated filesystem (database) and log the action.
    :param directory_name: The name of the directory to be deleted.
    """
    if fsDB:
        # Check if the directory exists in the database
        filters = {"oid": oid, "name": directory_name, "pid": pid}  # Assuming root directory
        directory_record = fsDB.read_data("directories", filters)
        
        if directory_record:
            # Delete the directory from the database
            fsDB.delete_data("directories", "name", directory_name)
            return {"message": f"Directory '{directory_name}' deleted from the database."}
        else:
            raise HTTPException(status_code=404, detail="Directory not found.")
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")