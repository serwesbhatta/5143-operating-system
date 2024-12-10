from .call_api import call_api
from .fs_state_manager import Fs_state_manager


def Run_history(index = None):
    if index == None:
        return {
            "status": "fail",
            "message": "\nPlease enter the index of the history to run the command you want."
        }

    index = index[0]

    try:
        i = int(index)
    except:
        return {
            "status": "fail",
            "message": "\nPlease enter index number."
        }

    oid = Fs_state_manager.get_oid()
    filters = {"oid": oid, "pid": 1, "name": "history.txt"}

    try:
        response = call_api("files", params=filters)

        if response["status"] == "success":
            content = response["message"][0]["contents"]

            lines = content.split("\n")

            for line in lines:
                if line.startswith(index + " "):
                    command = line[len(index):].strip()
                    command = command.strip().split()

                    main = command[0]
                    args = []

                    if len(command) > 1:
                        args = command[1:]

                    if main.startswith("!"):
                        index_cmd = [main[1:]]
                        index_response = Run_history(index_cmd)

                        if index_response["status"] == "success":
                            message = index_response["message"]
                            
                        return index_response

                    message = {
                        "main": main,
                        "args": args
                    }
                    return {
                        "status": "success",
                        "message": message
                    }

            return {
                "status": "fail",
                "message": "\nCannot find that command you were looking for."
            }

        else:
            message = response["message"]
            return {
                "status": "fail",
                "message": message
            }

    except:
        return {
            "status": "fail",
            "message": "\nCould not make a cal to api."
        }
