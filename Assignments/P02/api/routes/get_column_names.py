from fastapi import HTTPException
from database.sqliteCRUD import SqliteCRUD

def Get_column_names(fsDB: SqliteCRUD, table_name: str):
    """
    Get a list of files from the simulated filesystem (from the database).
    """
    if fsDB:
        try:
            files = fsDB.get_column_names(table_name)
            return files
        except:
            raise HTTPException(status_code=404, detail="Could not fetch column names")
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")

    