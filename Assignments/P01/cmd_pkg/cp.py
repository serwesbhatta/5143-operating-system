from .call_api import call_api
from .fs_state_manager import Fs_state_manager
from .file_path_helper import file_path_helper
from .dir_path_helper import dir_path_helper


def cp(params=None):
    if params == None or len(params) == 0:
        return {
            "status": "fail",
            "message": "\nPlease specify the source path and the target path",
        }
    
    if len(params) == 1:
        return {
            "status": "fail",
            "message": "\nPlease specify the destination path as well."
        }

    if len(params) > 2:
        return {
            "status": "fail",
            "message": "\nToo many path specified. Please specify only source and target path",
        }

    source_path = params[0]
    target_path = params[1]

    source_response = file_path_helper(source_path)

    if source_response["status"] == "success" and source_response["file_exist"] == True:
        target_response = dir_path_helper(target_path)

        if target_response["status"] == "success":
            oid = source_response["oid"]
            source_pid = source_response["pid"]
            source_filename = source_response["file_name"]

            target_pid = target_response["pid"]

            filters = {
                "oid": oid,
                "pid": source_pid,
                "name": source_filename,
                "target_pid": target_pid,
            }

            try:
                api_response = call_api("copy", "post", data=filters)
                
                if api_response["status"] == "success":
                    return {
                        "status": "success",
                        "message": ""
                    }
                
                message = api_response["message"]
                return {
                    "status": "fail",
                    "message": message
                }
            
            except:
                return {
                    "status": "fail",
                    "message": "\nCould not make a call to api"
                }
        else:
            return {
                "status": "fail",
                "message": f"\nTarget path {target_path} not found."
            }
    else:
        return {
            "status": "fail",
            "message": f"\nSource path {source_path} doesn't exist"
        }
    
