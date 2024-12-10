from fastapi import HTTPException
from datetime import datetime
from database.sqliteCRUD import SqliteCRUD

def Create_directory(fsDB: SqliteCRUD, oid:int, pid: int, directory_name: str):
    """
    Create a new directory in the simulated filesystem and log the action in the database.
    :param directory_name: The name of the new directory.
    :param pid: The ID of the parent directory.
    :param owner_id: The ID of the owner (optional).
    """
    if fsDB:
        # Check if the directory already exists
        filters = {"oid": oid, "name": directory_name, "pid": pid} 
        existing_dir = fsDB.read_data("directories", filters)
         
        if existing_dir:
            raise HTTPException(status_code=400, detail="Directory already exists.")
        
        # Insert the new directory into the database
        fsDB.insert_data(
            "directories", (None, pid, oid, directory_name, datetime.now(), datetime.now(),
            1, 0, 1, 1, 0, 1)  # Permissions and default values
        )
        
        return {
            "status": "success",
            "message": f"\nAPI: Directory '{directory_name}' created successfully."
            }
    else:
        return {
            "status": "fail",
            "message": "\nAPI: Database not initialized."
        }
