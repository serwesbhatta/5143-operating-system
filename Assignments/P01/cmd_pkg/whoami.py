from .fs_state_manager import Fs_state_manager
from .get_owner_name import get_owner_name

def whoami():
  current_oid = Fs_state_manager.get_oid()
  
  current_user = get_owner_name(current_oid)

  Fs_state_manager.set_current_user(current_user)

  return {
    "status": "success",
    "message": f"\n{current_user}"
  }