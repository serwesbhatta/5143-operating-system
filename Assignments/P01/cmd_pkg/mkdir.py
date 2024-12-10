from cmd_pkg.fs_state_manager import Fs_state_manager
from .call_api import call_api

def mkdir(params = None):
    if params == None or len(params) == 0:
        return {"status": "fail", "message": "\nError: No directory name specified."}

    directory_name = params[0]

    if "." in directory_name:
        return {
            "status": "fail",
            "message": "\nDirectory name cannot have extensions."
        }

    current_pid = Fs_state_manager.get_pid()
    oid = Fs_state_manager.get_oid()

    filters = {"oid": oid, "pid": current_pid, "name": directory_name}
    existing_dir = call_api("dirs", params=filters)

    if existing_dir["status"] == "success":
        return {
            "status": "fail",
            "message": f"\nError: Directory '{directory_name}' already exists in the current directory."
        }

    try:
        response = call_api("createDir", "post", data=filters)

        if response["status"] == "success":
            return {
                "status": "success",
                "message": f"\nDirectory '{directory_name}' created successfully.",
            }
    except:
        return {
            "status": "fail",
            "message": "\nCould not create the specified directory."
        }
