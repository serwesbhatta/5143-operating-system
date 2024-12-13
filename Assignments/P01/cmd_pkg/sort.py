from .fs_state_manager import Fs_state_manager
from .call_api import call_api
from .file_path_helper import file_path_helper

def sort(params=None, input = None):
    if params == None and input == None:
        return {
            "status": "fail",
            "message": "\nPlease specify the filename or the filepath",
        }
    
    if input == None:
        file_path = params[0]
    
        file_path_response = file_path_helper(file_path)

        if file_path_response["status"] == "fail":
            return {
                "status": "fail",
                "message": "\nFile not found",
            }
        
        oid = Fs_state_manager.get_oid()
        pid = Fs_state_manager.get_pid()
        file_name = file_path_response["file_name"]
        
        filters = {"oid": oid, "pid": pid, "name": file_name}

        try:
            get_response = call_api("files", params=filters)
        except:
            return {
                "status": "fail",
                "message": "\nCould not read file."
            }
            
        if get_response["status"] == "success":
            contents = get_response["message"][0]["contents"]
            split_contents = contents.split("\n")
            sorted_contents = sorted(split_contents)
            sorted_output = "\n".join(sorted_contents)

            filters = {"oid": oid, "pid": pid, "filepath": file_name, "content": sorted_output}
            
            try:
                put_response = call_api("write", "put", data=filters)
            except:
                return {
                    "status": "fail",
                    "message": "\nCould not write in file."
                }

            if put_response["status"] == "success":
                return {
                    "status": "success",
                    "message": ""
                }
            else:
                return {
                    "status": "fail",
                    "message": "\nCould not write in file."
                }
        else:
            return {
                "status": "fail",
                "message": "\nCould not read file."
            }
    else:
        input_content = input["message"]
        split_contents = input_content.split("\n")
        sorted_contents = sorted(split_contents)
        sorted_output = "\n".join(sorted_contents)

        return {
            "status": "success",
            "message": sorted_output
        }