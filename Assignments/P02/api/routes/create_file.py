from fastapi import HTTPException
from datetime import datetime

from database.sqliteCRUD import SqliteCRUD

CURRENT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def Create_file(fsDB: SqliteCRUD, oid: int, pid: int, name: str):
    """
    Create a new file in the simulated filesystem and record the action in the database.
    """
    if fsDB:
        filters = {"oid" : oid, 'pid': pid, 'name': name}

        existing_file = fsDB.read_data("files", filters)

        print("Database is initialized")

        if existing_file:
            return {"status ": "fail", "message": "File already exists"}
            # raise HTTPException(status_code=400, detail="File already exists.")

        print("Inserting Data")

        # Insert values corresponding to the specified columns
        values = (
            None, pid, oid, name, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, "",
            1, 1, 1, 1, 0, 1  # Permissions and default values
        )

        fsDB.insert_data("files", values)
        
        return {"status": "success", "message": f"File '{name}' created successfully."}
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")
