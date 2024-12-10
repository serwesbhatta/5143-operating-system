from database.sqliteCRUD import SqliteCRUD

def Get_parent_directory(fsDB: SqliteCRUD, id: int):
    if fsDB:
        try:
            response = fsDB.get_parent_directory(id)

            if response:
                pid = response["pid"]
                return {
                    "status": "success",
                    "message": pid
                }
        except:
            return {
                "status": "fail",
                "message": "Could not make a request to database to get parent id"
            }