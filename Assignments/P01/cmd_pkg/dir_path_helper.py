from .call_api import call_api
from .fs_state_manager import Fs_state_manager

def dir_path_helper(path: str):
    """
    Helper function to validate and navigate directory paths.

    :param path: The directory path to validate.
    :return: Directory ID if valid, None otherwise.
    """
    try:
        if len(path) == 0 or path == None:
            return {
                "status": "fail",
                "message": "\nPlease provide the path or the file name",
            }

        path_arr = path.split("/")
        oid = Fs_state_manager.get_oid()

        if path[0][0] == "/":
            pid = 1
            path_arr.pop(0)

        else:
            pid = Fs_state_manager.get_pid()

        directories_exist = False

        if len(path_arr) > 0:
            for dir in path_arr:
                if dir == "..":
                    try:
                        response = call_api("parentDir", params={"id": pid})

                        if response["status"] == "success":
                            pid = response["message"]
                        else:
                            return {
                                "status": "fail",
                                "message": "\nNo parent directory found"
                            }
                    except:
                        return {
                            "status": "fail",
                            "message": "\nCannot resolve parent directory"
                        }

                else:
                    filters = {"oid": oid, "pid": pid, "name": dir}

                    try:
                        response = call_api("dirs", params=filters)

                        if response["status"] == "success":
                            response_message = response["message"]
                            pid = response_message[0]["id"]

                        else:
                            return {
                                "status": "fail",
                                "message": "Path not found",
                                "directories_exist": directories_exist,
                                "pid": pid,
                                "oid": oid,
                            }

                    except:
                        return {
                            "status": "fail",
                            "message": "Path not found",
                            "directories_exist": directories_exist,
                            "pid": pid,
                            "oid": oid,
                        }
        else:
            return {
                "status": "fail",
                "message": "Path not found",
                "directories_exist": directories_exist,
                "pid": pid,
                "oid": oid,
            }

        directories_exist = True

        return {
            "status": "success",
            "message": "Path found",
            "directories_exist": directories_exist,
            "pid": pid,
            "oid": oid,
        }

    except Exception as e:
        print(f"Error in file_path_helper: {e}")
        return ""
