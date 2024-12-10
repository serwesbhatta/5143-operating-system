from cmd_pkg.fs_state_manager import Fs_state_manager
from datetime import datetime
from .file_path_helper import file_path_helper
from .call_api import call_api

CURRENT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def touch(params = None):
    """Create a new file or update the timestamp of an existing file."""
    if not params:
        print("\nPlease specify the filename or the filepath")
        return {
            "status": "fail",
            "message": "\nPlease specify the filename or the filepath",
        }

    file_path = params[0]
    file_path_arr = file_path.split("/")

    if len(file_path_arr) > 1:
        response = file_path_helper(file_path)

        if response["directories_exist"] and response["file_exist"]:
            print("\nFile already exist")
        elif response["directories_exist"]:
            oid = response["oid"]
            pid = response["pid"]
            file_name = file_path_arr[-1]

            if "." not in file_name:
                file_name = file_name + ".txt"

            new_file_filters = {"oid": oid, "pid": pid, "name": file_name}
            new_file_response = call_api("touch", "post", data=new_file_filters)
            if new_file_response["status"] == "success":
                return {
                    "status": "pass",
                    "message": ""
                }
            else:
                return {"status": "fail", "message": "\nCannot create the file"}
        else:
            return {"status": "fail", "message": "\nDirectory not found"}

    else:
        pid = Fs_state_manager.get_pid()
        oid = Fs_state_manager.get_oid()
        file_name = file_path

        if "." not in file_name:
            file_name = file_name + ".txt"

        filters = {"oid": oid, "pid": pid, "name": file_name}

        new_file_response = call_api("touch", "post", data=filters)

        if new_file_response["status"] == "success":
            return {
                "status": "success",
                "message": ""
            }
        else:
            return {"status": "fail", "message": "\nCannot create the file"}
