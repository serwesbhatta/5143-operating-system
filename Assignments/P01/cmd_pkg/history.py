from datetime import datetime
from cmd_pkg.fs_state_manager import Fs_state_manager
from .call_api import call_api

# Get current timestamp for logging or history entries
CURRENT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def history(cmd=None):
    """
    Retrieve or create a history file for each user based on their OID (owner ID).
    """
    try:
        # Retrieve owner ID for the current user and create a unique filename
        oid = Fs_state_manager.get_oid()
        filename = "history.txt"
        
        # Define the parameters to check if the file exists
        history_params = {"pid": 1, "name": filename, "oid": oid}
        
        # Attempt to fetch history file content via API'
        existing_history = call_api("files", "get", params=history_params)

        if existing_history["status"] == "success":
            if cmd:
                previous_contents = existing_history["message"][0]["contents"]
                lines = previous_contents.strip().split("\n")
                count = len(lines)

                new_contents = previous_contents + "\n" + str(count) + " " + cmd

                update_history_data = {"oid": oid, "pid": 1, "filepath": filename, "content": new_contents}

                response = call_api("write", "put", data=update_history_data)

                if response is None:
                    print("Failed to update history.")
            else:
                response = call_api("files", params=history_params)
                if response["status"] == "success":
                    return {
                        "status": "success",
                        "message": response["message"][0]["contents"]
                    }
                else:
                    return {
                        "status": "fail",
                        "message": ""
                    }
        else:
            contents = ""
            if cmd:
                contents += "\n" + "0 " + cmd

            new_history_data = {"oid": oid, "pid": 1, "name": "history.txt"}
            create_response = call_api("touch", "post", data=new_history_data)

            if create_response == 200:
                print(f"Failed to create history file")
            else:
                update_history_data = {"oid": oid, "pid": 1, "filepath": filename, "content": contents}

                response = call_api("write", "put", data=update_history_data)

                if response is None:
                    print("Failed to update history.")
        
    except Exception as e:
        print(f"Error accessing history file: {e}")
    
    return ""  # Optional: return a status message or content

