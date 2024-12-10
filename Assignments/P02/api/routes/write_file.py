from fastapi import HTTPException
from database.sqliteCRUD import SqliteCRUD
from .create_file import Create_file
from .encoder_decoder import Encode
from .get_column_names import Get_column_names

def Write_file(fsDB: SqliteCRUD, oid:int, pid: int, filepath: str, content: str):
    """
    Writes data to a file and logs the write operation in the database.
    :param filepath: The path of the file to write to.
    :param content: The content to write to the file.
    :param oid: The ID of the user attempting to write to the file.
    """
    if fsDB:
        # Check if the file exists and fetch it
        filters = {"oid": oid, "name": filepath, "pid": pid}

        file_record = fsDB.read_data("files", filters)
        
        if file_record:
            column_names = Get_column_names(fsDB, "files")
            file = [dict(zip(column_names, row)) for row in file_record]
            file_id = file[0]["id"] # File ID
            print(f"File id:  {file_id}")
            owner_id = file[0]["oid"]  # Owner ID
            print(f"Owner Id: {owner_id}")
            write_permission = file[0]["write_permission"]  # Write permission
            world_write = file[0]["world_write"]  # World write permission

            # Check if the user has permission to write
            if (oid == owner_id and write_permission == 1) or world_write == 1:
                # Use the generic update_data function to update the contents
                # Change content to blob content
                content = Encode(content) 
                print(content)
                update_status = fsDB.update_data("files", "contents", content, "id", file_id)
                if update_status["success"]:
                    print("\n\n\n\nupdated\n\n\n\n")
                    return {
                        "status": "success",
                        "message": f"Content written to file '{filepath}' successfully."
                        }
                else:
                    raise HTTPException(status_code=500, detail=update_status["message"])
            else:
                raise HTTPException(status_code=403, detail="Permission denied to write to the file.")
        else:
            Create_file(fsDB, oid, pid, filepath)
            Write_file(fsDB, oid, pid, filepath, content)
            return {
                "status": "success",
                "message": f"Created new file {filepath} sucessfully with the required content."
                }
    else:
        raise HTTPException(status_code=500, detail="Database not initialized.")