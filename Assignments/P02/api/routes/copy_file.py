from datetime import datetime
from database.sqliteCRUD import SqliteCRUD
from .get_files import Get_files
from .encoder_decoder import Encode

CURRENT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def Copy_file(
    fsDB: SqliteCRUD,
    oid: int,
    pid: int,
    name: str,
    target_pid: int,
):
    """
    Create a new file in the simulated filesystem and record the action in the database.
    """
    if fsDB:
        try:
            source_file = Get_files(fsDB, oid, pid, name)
            source_file = source_file["message"]

        except:
            return {"status": "fail", "message": "\nUnable to read source file."}

        if source_file:
            size = source_file[0]["size"]
            content = source_file[0]["contents"]
            content = Encode(content)
            read_permission = source_file[0]["read_permission"]
            write_permission = source_file[0]["write_permission"]
            execute_permission = source_file[0]["execute_permission"]
            world_read = source_file[0]["world_read"]
            world_write = source_file[0]["world_write"]
            world_execute = source_file[0]["world_execute"]

            try:
                target_file = Get_files(fsDB, oid, target_pid, name)

                if target_file["status"] == "success":
                    return {
                        "status": "fail",
                        "message": "\nFile already exists."
                    }
                
                else:
                    values = (
                        None,
                        target_pid,
                        oid,
                        name,
                        size,
                        CURRENT_TIMESTAMP,
                        CURRENT_TIMESTAMP,
                        content,
                        read_permission,
                        write_permission,
                        execute_permission,
                        world_read,
                        world_write,
                        world_execute,
                    )

                    try:
                        fsDB.insert_data("files", values)

                        return {
                            "status": "success",
                            "message": f"\nFile '{name}' created successfully.",
                        }
                    except:
                        return {
                            "status": "fail",
                            "message": f"\nUnable to create the file {name}.",
                        }
            except:
                return {"status": "fail", "message": "\nUnable to read target file."}

        return {"status": "fail", "message": "\nFile doesn't exist"}

    else:
        return {"status": "fail", "message": f"\nDatabase is not initialized."}
