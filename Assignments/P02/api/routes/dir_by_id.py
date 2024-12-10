from fastapi import HTTPException
from database.sqliteCRUD import SqliteCRUD
from .convert_to_dictionary import Convert_to_dictionary


def Dir_by_id(fsDB: SqliteCRUD, oid: int, id: int):
    """
    List all directories under a specific parent directory in the simulated filesystem.
    :param pid: The ID of the parent directory (default is root directory with ID 1).
    """
    filters = {"oid": oid, "id": id}

    if fsDB:
        # Fetch directories under the specified parent directory
        directories = fsDB.read_data("directories", filters)

        if directories:
            result = Convert_to_dictionary("directories", directories)
            return {
                "status": "success",
                "message": result
            }
        else:
            return {
                "status": "fail",
                "message": "\nAPI: No directories found under the specified parent directory.",
            }
    else:
        return {
            "status": "fail",
            "message": "\nAPI: Database not initialized.",
        }
        raise HTTPException(status_code=500, detail="D")
