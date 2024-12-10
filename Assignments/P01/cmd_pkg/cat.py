# from .encoder_decoder import decode
from cmd_pkg.fs_state_manager import Fs_state_manager
from .call_api import call_api


def cat(params=None):
    """Display the contents of one or more files."""
    if not params:
        return {"status": "fail", "message": "\nError: No file specified."}

    total_file_contents = ""

    for param in params:
        filename = param
        current_pid = Fs_state_manager.get_pid()
        oid = Fs_state_manager.get_oid()
        filters = {"name": filename, "pid": current_pid, "oid": oid}

        try:
            response = call_api("files", params=filters)
            
        except:
            return {"status": "fail", "message": "\nCould not make a call to the api"}

        if response["status"] == "success":
            content = response["message"][0]["contents"]
            total_file_contents += content
        
        else:
            return {"status": "fail", "message": "\nDidn't find the file you were looking for."}

    return {
        "status": "success",
        "message": f"\n{total_file_contents}"
    }
