from cmd_pkg.fs_state_manager import Fs_state_manager
from .call_api import call_api
from .file_path_helper import file_path_helper


def more(params=None):
    """DESCRIPTION: The `more` command views the contents of a file one screen at a time.
    USAGE: more [FILE]
    EXAMPLE:
        > more file1.txt
        Displays the content of file1.txt, one screen at a time.
    """
    if not params:
        return {"status": "fail", "message": "\nError: No file specified."}
    if len(params) > 1:
        return {"status": "fail", "message": "\nError: Only one file at a time."}
    
    file_path = params[0]

    try:
        file_path_response = file_path_helper(file_path)
    except:
        return {"status": "fail", "message": "\nError: Could not call api."}
    
    if file_path_response["status"] == "fail":
        return {"status": "fail", "message": "\nError: File not found."}
    
    file_name = file_path_response["file_name"]
    current_pid = Fs_state_manager.get_pid()
    oid = Fs_state_manager.get_oid()

    filters = {"name": file_name, "pid": current_pid, "oid": oid}

    try:
        response = call_api("files", params=filters)
    except Exception as e:
        return {
            "status": "fail",
            "message": f"\nCould not make a call to the api: {str(e)}",
        }

    if response["status"] == "success":
        lines = response["message"][0]["contents"].split("\n")
        page_size = 35  # number of lines per page
        num_pages = (
            len(lines) + page_size - 1
        ) // page_size  # Calculate the number of pages
        for i in range(num_pages):
            start_line = i * page_size
            end_line = start_line + page_size
            page_content = "\n".join(lines[start_line:end_line])
            print(f"\n--- Showing lines {start_line+1} to {end_line} ---\n")
            print(page_content)
            if i < num_pages - 1:  # Check if not the last page
                input("Press Enter to see the next page, type 'q' to quit: ")
                if input().lower() == "q":
                    break
        return {"status": "success", "message": "\nEnd of file."}
    else:
        return {
            "status": "fail",
            "message": "\nDidn't find the file you were looking for.",
        }
