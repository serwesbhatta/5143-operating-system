from cmd_pkg.fs_state_manager import Fs_state_manager
from .call_api import call_api

def pwd(params=None):
    """Print the current working directory."""
    # Get the current path from the file system state manager
    id = Fs_state_manager.get_pid()
    oid = Fs_state_manager.get_oid()
    dirs = []

    try:
        while id != 1:
            filters = {"oid": oid, "id": id}
            response = call_api("dirById", params=filters)

            if response["status"] == "success":
                directory = response["message"]
                dir_name = directory[0]["name"]
                dirs.append(dir_name)
                id = directory[0]["pid"]

            else:
                return {
                    "status": "fail",
                    "message": "\nPath cannot be found"
                }

        dirs.reverse()

        if len(dirs) > 0:
            path = "~/"+ "/".join(dirs)
            Fs_state_manager.set_path(path)

        else:
            path = "~"
            Fs_state_manager.set_path(path)

        return {
            "status": "success",
            "message": f"\n{path}"
        }

    except:
        return {
            "status": "fail",
            "message": "Cannot process print working directory"
        }
