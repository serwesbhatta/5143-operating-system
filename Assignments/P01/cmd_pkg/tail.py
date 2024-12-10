from .call_api import call_api
from .fs_state_manager import Fs_state_manager
from .get_flags import get_flags


def tail(params=None, input=None):
    """Display the first N lines of a file."""
    if params == None and input == None:
        return {"status": "fail", "message": "\nError: No file specified."}

    file_name = ""
    num_lines = 10  # Default to 10 if no -n option is provided

    allowed_flags = ["n"]
    flags_response = get_flags(allowed_flags, params)
    flags = flags_response["flags"]

    if flags_response["invalid_flags"]:
        return {"status": "fail", "message": "\nOnvalid flags"}

    if flags:
        flag_index = flags_response["flags_index"][0]
        params.pop(flag_index)

        if params == []:
            return {"status": "fail", "message": "\nPlease specify the number"}
        num_lines_index = flag_index
        try:
            num_lines = int(params[num_lines_index])
            if num_lines < 1:
                return {
                    "status": "fail",
                    "message": "\nError: Number of lines must be a positive integer.",
                }
        except ValueError:
            return {
                "status": "fail",
                "message": "\nError: Invalid number of lines specified. It must be an integer.",
            }

        params.pop(flag_index)

        if params == []:
            return {"status": "fail", "message": "\nPlease enter the file name as well"}

        file_name = params[0]

    elif flags == [] and len(params) > 1:
        return {
            "status": "fail",
            "message": "\nToo many parameters",
        }
    
    else:
        file_name = params[0]

    pid = Fs_state_manager.get_pid()
    oid = Fs_state_manager.get_oid()

    filters = {"oid": oid, "pid": pid, "name": file_name}

    try:
        response = call_api("files", params=filters)

        # Fetch file contents from the database
        if response["status"] == "success":
            file_contents = response["message"][0]["contents"]

            if file_contents is not None:
                lines = file_contents.split("\n")
                message = "\n".join(lines[-num_lines:])
                return {"status": "success", "message": f"\n{message}"}
            else:
                return {
                    "status": "fail",
                    "message": f"\nError: Could not read the contents of '{file_name}'.",
                }
        else:
            return {
                "status": "fail",
                "message": f"\nError: File '{file_name}' does not exist in the current directory.",
            }
    except:
        return {"status": "fail", "message": "\nCould not make a call to api"}
