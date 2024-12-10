from fastapi import HTTPException
from database.sqliteCRUD import SqliteCRUD
from .get_column_names import Get_column_names
from .convert_to_dictionary import Convert_to_dictionary

def List_directories(fsDB: SqliteCRUD, oid: int, pid: int, name: str = None):
    """
    List all directories under a specific parent directory in the simulated filesystem.
    :param pid: The ID of the parent directory (default is root directory with ID 1).
    """
    if name:
        filters = {"oid": oid, "name": name, "pid": pid}
    elif pid:
        filters = {"oid": oid, "pid": pid}
    else:
        print("Please use the pid")
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
            "message": "\nAPI: Database not initialized."
        }
