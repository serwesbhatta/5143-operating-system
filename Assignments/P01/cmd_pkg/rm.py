from .call_api import call_api
from cmd_pkg.fs_state_manager import Fs_state_manager

def rm(params=None):
    """Remove a file from the current directory."""
    if params == None or len(params) == 0:
        return {"status": "fail", "message": "\nError: No file name specified."}

    file_name = params[0]
    pid = Fs_state_manager.get_pid()
    oid = Fs_state_manager.get_oid()
    filters = {"oid": oid, "pid": pid, "name": file_name}
    try:
        existing_file = call_api("files", params=filters)

        if existing_file["status"] == "success":
            response = call_api("rm", "delete", data=filters)  # Assuming name is unique per directory
            
            if response["status"] == "success":
                return {
                    "status": "success",
                    "message": f"\nSuccessfully deleted {file_name}."
                }

            else:
                return {
                    "status": "fail",
                    "message": f"\nCould not delete {file_name}."
                }
        else:
            return {
                "status": "fail",
                "message": f"Error: File '{file_name}' does not exist in the current directory.",
            }
            print()
    except:
        return {
            "status": "fail",
            "message": "\nCould not make a call to the api."
        }
    
