from .call_api import call_api

def get_owner_name(oid):
    """Fetch the username of the owner based on the owner_id from the 'users' table."""
    filters = {"user_id": oid}
    user_record = call_api("users", params=filters)
    if user_record["status"] == "success":
        return user_record["message"][0]["username"]
    return "unknown"
