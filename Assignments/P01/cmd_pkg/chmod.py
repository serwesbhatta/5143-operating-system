from .call_api import call_api
from .fs_state_manager import Fs_state_manager
from .file_path_helper import file_path_helper
from .dir_path_helper import dir_path_helper

def chmod(params=None):
   if params == None:
      return {
         "status": "fail",
         "message": "\nPlease write the permission to be set with the filenamne"
      }
   
   if len(params) < 2 or len(params) > 2:
      return {
         "status": "fail",
         "message": "\nPlease specify permission and then filename."
      }

   try:
      permission = int(params[0])
   except:
     return {
          "status": "fail",
          "message": "\nPlease enter permission after chmod command."
     }
   
   mode = params[0]
   path = params[1]
   name = ""
   file_exist = False
   
   file_path_response = file_path_helper(path)

   if file_path_response["status"] == "success" and file_path_response["file_exist"]:
      name = file_path_response["file_name"]
      file_exist = True

   else:
      dir_path = path
      dir_path_response = dir_path_helper(dir_path)

      if dir_path_response["status"] == "success" and dir_path_response["directories_exist"]:
         name = params[1].split("/")[-1]

      else:
         return {
            "status": "fail",
            "message": "\nPath not found."
         }
   
   oid = Fs_state_manager.get_oid()
   pid = Fs_state_manager.get_pid()

   filters = {"file": file_exist, "oid": oid, "pid": pid, "name": name, "mode": mode}

   try:
      response = call_api("setpermissions", "put", data=filters)

      if response["status"] == "success":
         return {
            "status": "success",
            "message": response["message"]
         }
   except:
      return {
         "status": "fail",
         "message": "\nUnable to call api"
      }