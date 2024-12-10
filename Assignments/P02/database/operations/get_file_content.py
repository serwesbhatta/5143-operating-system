import sqlite3
from .read_data import Read_data

def Get_file_content(cursor, filters):
        """
        Retrieves file content and checks permissions.
        """
        try:
            # Fetch file details
            print("before file record")
            file_record = Read_data(cursor, "files", filters)

            print(f"File record: {file_record}")

            if file_record:
                owner_id = file_record[0][2]  # Owner ID
                read_permission = file_record[0][8]  # Read permission
                world_read = file_record[0][11]  # World read permission

                # Check if the user has permission to read
                if (filters["oid"] == owner_id and read_permission == 1) or world_read == 1:
                    content = file_record[0][7]  # File content
                    return {"success": True, "status": 200, "content": content}
                else:
                    return {"success": False, "status": 403, "message": "Permission denied."}
            else:
                return {"success": False, "status": 404, "message": "File not found."}
        
        except sqlite3.Error as e:
            return {"success": False, "status": 500, "message": f"Database error: {e}"}