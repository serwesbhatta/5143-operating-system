from database.sqliteCRUD import SqliteCRUD


def Set_permissions(
    fsDB: SqliteCRUD, file: bool, oid: int, pid: int, name: str, mode: str
):
    if fsDB:
        table_name = "directories"

        if file:
            table_name = "files"

        owner_permission = int(mode[0])
        owner_permission = format(owner_permission, "b").zfill(3)
        world_permnission = int(mode[2])
        world_permission = format(world_permnission, "b").zfill(3)

        permissions = {
            "owner_read": int(owner_permission[0]),
            "owner_write": int(owner_permission[1]),
            "owner_execute": int(owner_permission[2]),
            "world_read": int(world_permission[0]),
            "world_write": int(world_permission[1]),
            "world_execute": int(world_permission[2]),
        }
        print(permissions)

        filters = {"oid": oid, "pid": pid, "name": name}

        response = fsDB.set_permissions(table_name, permissions, filters)

        if response["status"] == "success":
            return {
                "status": "success",
                "message": f"\nChanged the permissions of '{name}' successfully"
            }

        else:
            message = response["message"]
            return {
                "status": "fail",
                "message": f"\n{message}"
            }
