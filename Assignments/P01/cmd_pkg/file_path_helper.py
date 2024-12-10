from .call_api import call_api
from .fs_state_manager import Fs_state_manager


def file_path_helper(path: str = None):
    """
    Helper function to validate file paths.

    :param path: The file path to validate.
    :return: Tuple (is_file, directory_id, filename) if valid, None otherwise.
    """
    try:
        if len(path) == 0 or path == None:
            return {
                "status": "fail",
                "message": "Please provide the path or the file name",
            }

        path_arr = path.split("/")
        file_name = path_arr.pop()

        oid = Fs_state_manager.get_oid()
        pid = Fs_state_manager.get_pid()

        if path[0][0] == "/":
            pid = 1
            path_arr.pop(0)

        directories_exist = False
        file_exist = False

        if len(path_arr) > 0:
            for dir in path_arr:
                if dir == "..":
                    try:
                        response = call_api("parentDir", params={"id": pid})
                    except:
                        return {
                            "status": "fail",
                            "directories_exist": directories_exist,
                            "file_exist": file_exist,
                            "file_name": file_name,
                            "pid": pid,
                            "oid": oid,
                        }
                    if response:
                        pid = response["pid"]

                else:
                    filters = {"oid": oid, "pid": pid, "name": dir}

                    try:
                        response = call_api("dirs", params=filters)
                        if response["status"] == "success":
                            # Here we are using pid to id and at the final point as welll we are using piod
                            # it is beacuse when we are handling files we need the id of the folder to be pid
                            # of the file.

                            pid = response["message"][0]["id"]

                    except:
                        return {
                            "status": "fail",
                            "directories_exist": directories_exist,
                            "file_exist": file_exist,
                            "file_name": file_name,
                            "pid": pid,
                            "oid": oid,
                        }

        directories_exist = True

        filters = {"oid": oid, "pid": pid, "name": file_name}

        try:
            response = call_api("files", params=filters)

            if response["status"] == "success":
                file_exist = True

        except:
            pass
 
        return {
            "status": "success",
            "directories_exist": directories_exist,
            "file_exist": file_exist,
            "file_name": file_name,
            "pid": pid,
            "oid": oid,
        }

    except Exception as e:
        print(f"Error in file_path_helper: {e}")
        return ""
