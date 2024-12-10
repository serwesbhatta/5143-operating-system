from .fs_state_manager import Fs_state_manager
from .dir_path_helper import dir_path_helper
from .pwd import pwd

def cd(params=None):
    if params == None:
        return {
            "status": "fail",
            "message": "\nPlease specify the path"
        }

    path = params[0]

    pid = Fs_state_manager.get_pid()

    if path == "~":
        pid = 1
        Fs_state_manager.set_pid(pid)
        pwd()
        return {
            "status": "success",
            "message": ""
        }

    if pid == 1 and path == "..":
        return {
            "status": "fail",
            "message": "\nYou are already in the root directory."
        }

    response = dir_path_helper(path)

    if response["status"] == "success":
        if response["directories_exist"]:
            pid = response["pid"]

            Fs_state_manager.set_pid(pid)

            pwd()

            return {
                "status": "success",
                "message":""
            }

        else:
            return {
                "status": "fail",
                "message": "\nPath doesn't exist"
            }
    else:
        message = response["message"]
        return {"status": "fail", "message": f"\n{message}"}
