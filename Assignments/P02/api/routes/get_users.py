from database.sqliteCRUD import SqliteCRUD
from fastapi import HTTPException
from .get_column_names import Get_column_names


def Get_users(fsDB: SqliteCRUD, user_id: int = None):
    if id:
        filters = {"user_id": user_id}
    else:
        filters = {}

    if fsDB:
        try:
            files = fsDB.read_data("users", filters)
        except:
            raise HTTPException(status_code=404, detail="Could not read data")
        if files:
            column_names = Get_column_names(fsDB, "users")
            rows = [dict(zip(column_names, row)) for row in files]
            return {
                "status": "success",
                "message": rows
            }
        else:
            return {"status": "fail", "message": "\nAPI: No files found"}
    else:
        return {"status": "fail", "message": "\nAPI: Database not initialized."}
