from cmd_pkg.fs_state_manager import Fs_state_manager
from .dir_path_helper import dir_path_helper
from .call_api import call_api

def mkdir(params = None):
    if params == None or len(params) == 0:
        return {"status": "fail", "message": "\nError: No directory name specified."}

    directory_path = params[0]

    directory_path_arr = directory_path.split("/")
    directory_name = directory_path_arr.pop()
    directory_path = "/".join(directory_path_arr)

    if "." in directory_name:
        return {
            "status": "fail",
            "message": "\nDirectory name cannot have extensions."
        }

    try:
        directory_path_response = dir_path_helper(directory_path)
    except:
        return {
            "status": "fail",
            "message": "\nCannot look for the specified directory."
        }
    
    if directory_path_response["status"] == "fail":
        return {
            "status": "fail",
            "message": f"\nError: {directory_path_response['message']}"
        }

    pid = directory_path_response["pid"]
    oid = directory_path_response["oid"]

    filters = {"oid": oid, "pid": pid, "name": directory_name}
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
