from .get_flags import get_flags
from .call_api import call_api
from .fs_state_manager import Fs_state_manager
from .file_path_helper import file_path_helper
from .dir_path_helper import dir_path_helper


def rm(params=None):
    if not params:
        return {
            "status": "fail",
            "message": "Please specify a file or directory to remove.",
        }
    allowed_flags = ["r", "f"]
    flags_response = get_flags(allowed_flags, params)

    if flags_response["invalid_flags"]:
        return {"status": "fail", "message": "Invalid flags provided for rm command."}

    flags = flags_response["flags"]
    recursive = "r" in flags
    force = "f" in flags
    params = [param for param in params if not param.startswith("-")]

    if not params:
        return {
            "status": "fail",
            "message": "Please specify a file or directory to remove.",
        }

    if len(params) > 1:
        return {
            "status": "fail",
            "message": "Too many arguments provided for rm command.",
        }

    target_path = params[0]

    # Edge cases for special paths
    if target_path in [".", "..", "~", ""]:
        return {
            "status": "fail",
            "message": f"Cannot remove reserved path '{target_path}'.",
        }

    try:
        file_path_response = file_path_helper(target_path)
    except:
        return {
            "status": "fail",
            "message": "Cannot process file path.",
        }

    if file_path_response["status"] == "fail":
        return {
            "status": "fail",
            "message": "Cannot process file path.",
        }

    if file_path_response["status"] == "success" and file_path_response["file_exist"]:
        file_name = file_path_response["file_name"]
        file_oid = file_path_response["oid"]
        file_pid = file_path_response["pid"]

        delete_file_response = call_api(
            "rm", "delete", data={"oid": file_oid, "pid": file_pid, "name": file_name}
        )

        if delete_file_response["status"] == "fail":
            return {
                "status": "success",
                "message": f"\nCould not remove {file_name}.",
            }

    try:
        dir_path_response = dir_path_helper(target_path)
    except:
        return {
            "status": "fail",
            "message": "Cannot process target path.",
        }
    if dir_path_response["status"] == "fail":
        return {
            "status": "fail",
            "message": "\nCannot process target path.",
        }

    if not recursive:
        return {
            "status": "fail",
            "message": "\nCannot remove directory without -r flag.",
        }
    else:
        dir_pid = dir_path_response["pid"]
        dir_oid = dir_path_response["oid"]

        try:
            get_files_response = call_api(
                "files", params={"oid": dir_oid, "pid": dir_pid}
            )
        except:
            return {
                "status": "fail",
                "message": "\nCannot get files in directory.",
            }
        if get_files_response["status"] == "success" and get_files_response["message"]:
            files = get_files_response["message"]
            for file in files:
                try:
                    delete_file_response = call_api(
                        "rm", "delete",
                        data={"oid": dir_oid, "pid": dir_pid, "name": file["name"]},
                    )
                except:
                    return {
                        "status": "fail",
                        "message": "\nCould not remove file.",
                    }

        try:
            get_dir_response = call_api("dirs", params={"oid": dir_oid, "pid": dir_pid})
        except:
            return {
                "status": "fail",
                "message": "\nCannot get directories in directory.",
            }
        if get_dir_response["status"] == "success" and get_dir_response["message"]:
            dirs = get_dir_response["message"]
            for dir in dirs:
                try:
                    delete_subdir_response = rm(
                        params=[
                            f"{target_path}/{dir['name']}",
                            "-rf",
                            "-rf" if force else "-r",
                        ]
                    )
                except:
                    return {
                        "status": "fail",
                        "message": "\nCould not remove subdirectory.",
                    }
        try:
            target_path_arr = target_path.split("/")
            dir_name = target_path_arr[-1]

            get_dir = call_api(
                "dirById",
                params={"oid": dir_oid, "id": dir_pid},
            )

            dir_pid = get_dir["message"][0]["pid"]
            dir_oid = get_dir["message"][0]["oid"]

            delete_dir_response = call_api(
                "deleteDir", "delete",
                data={"oid": dir_oid, "pid": dir_pid, "name": dir_name},
            )
            if delete_dir_response["status"] == "fail" and not force:
                return {
                    "status": "fail",
                    "message": f"Could not remove directory: {target_path}.",
                }
        except:
            if not force:
                return {
                    "status": "fail",
                    "message": f"Error removing directory: {target_path}.",
                }

        return {"status": "success", "message": ""}
