from .call_api import call_api
from .fs_state_manager import Fs_state_manager
from .get_flags import get_flags
import re


def grep(params=None, input=None):
    if params == None and input == None:
        return {
            "status": "fail",
            "message": "\nPlease specify the pattern and the filename",
        }
    elif len(params) == 1 and input == None:
        return {
            "status": "fail",
            "message": "\nPlease specify the pattern first and file after that.",
        }
    elif input is not None and len(params) == 0:
        return {"status": "fail", "message": "\nPlease specify the pattern"}

    l_flag = False
    i_flag = False
    c_flag = False

    allowed_flags = ["l", "i", "c"]
    flags_response = get_flags(allowed_flags, params)
    flags = flags_response["flags"]

    if flags_response["invalid_flags"]:
        return {"status": "fail", "message": "\nOnvalid flags"}

    if flags:
        if "l" in flags:
            l_flag = True
        if "i" in flags:
            i_flag = True
        if "c" in flags:
            c_flag = True
        params = [param for param in params if not param.startswith("-")]

    pattern = params[0]
    params.pop(0)

    # Validate or preprocess the pattern
    try:
        re.compile(pattern)
    except re.error:
        return {"status": "fail", "message": f"\nInvalid pattern: '{pattern}'."}

    contents = ""
    message = ""
    match_files = []
    counts = {}
    count_int = 0

    if input == None:
        params = [element.rstrip(",") for element in params]
        for param in params:
            filename = param
            oid = Fs_state_manager.get_oid()
            pid = Fs_state_manager.get_pid()

            filters = {"oid": oid, "pid": pid, "name": filename}

            try:
                response = call_api("files", params=filters)

                if response["status"] == "success":
                    contents = response["message"][0]["contents"] + "\n"
                    lines = contents.split("\n")
                    filename_added = False

                    for line in lines:
                        result = ""
                        if i_flag:
                            result = bool(re.search(pattern, line, re.IGNORECASE))
                        else:
                            result = bool(re.search(pattern, line))

                        if result == True:
                            if not filename_added:
                                match_files.append(param)
                                counts[param] = 0
                                filename_added = True
                            counts[param] += 1
                            message += "\n" + line

                else:
                    return {
                        "status": "fail",
                        "message": f"\nFile '{filename}' doesn't exist.",
                    }
            except:
                return {"status": "fail", "message": "\nCannot make a call to api."}
    else:
        contents = input["message"]

        lines = contents.split("\n")
        filename_added = False

        for line in lines:
            result = ""
            if i_flag:
                result = bool(re.search(pattern, line, re.IGNORECASE))
            else:
                result = bool(re.search(pattern, line))
            if result == True:
                count_int += 1
                message += "\n" + line

    final_message = ""

    if flags != []:
        if l_flag and input == None:
            final_message += "\n" + "\n".join(match_files)
        if c_flag and input == None:
            if len(counts) > 1:
                for key, value in counts.items():
                    final_message += f"\n{key} : {value}"
            elif len(params) == 1 and params[0] in counts:
                final_message += f"\n{params[0]} : {counts[params[0]]}"
        if l_flag and input != None:
            final_message = ""
        if c_flag and input != None:
            final_message = f"\n{count_int}"
    else:
        final_message = message

    return {"status": "success", "message": final_message}
