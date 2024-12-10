from .call_api import call_api
from .fs_state_manager import Fs_state_manager
from .get_flags import get_flags


def wc(params=None, input=None):
    if params == None and input == None:
        return {"status": "fail", "message": "\nPlease enter filename."}

    content = ""
    l_flag = False
    w_flag = False

    allowed_flags = ["l", "w"]
    flags_response = get_flags(allowed_flags, params)
    flags = flags_response["flags"]

    if flags_response["invalid_flags"]:
        return {"status": "fail", "message": "\nOnvalid flags"}
    
    if "l" in flags and "w" in flags:
        l_flag = True
        w_flag = True
        if "-lw" in params:
            params.remove("-lw")
        else:
            params.remove("-l")
            params.remove("-w")

    elif "l" in flags:
        l_flag = True
        params.remove("-l")

    elif "w" in flags:
        w_flag = True
        params.remove("-w")

    if len(params) == 0:
        return {
            "status": "fail",
            "message": "\nPlease enter the file name."
        }

    if input:
        content = input["message"]
    else:
        file_name = params[0]
        oid = Fs_state_manager.get_oid()
        pid = Fs_state_manager.get_pid()
        filters = {"oid": oid, "pid": pid, "name": file_name}

        try:
            response = call_api("files", params=filters)

            if response["status"] == "success":
                content = response["message"][0]["contents"]
            
            else:
                return {
                    "status": "fail",
                    "message": "\nCannot find the required file."
                }

        except:
            return {
                "status": "fail",
                "message": "\nUnable to make a call to api."
            }

    result = "\n"

    if flags:
        lines = content.split("\n")
        if l_flag:
            num_lines = len(lines)
            result += f"Lines: {num_lines}\t"
        if w_flag:
            num_words = sum(len(line.split()) for line in lines)
            result += f"Words: {num_words}\t"
        return {
            "status": "success",
            "message": result
        }
    else:
        lines = content.split("\n")
        num_lines = len(lines)
        num_words = sum(len(line.split()) for line in lines)
        num_characters = sum(len(line) for line in lines)

        result = f"\nLines: {num_lines}\tWords: {num_words}\tCharacters: {num_characters}"

        return {
            "status": "success",
            "message": result
        }
    