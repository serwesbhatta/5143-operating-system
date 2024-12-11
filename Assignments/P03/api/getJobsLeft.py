import requests

def getJobsLeft(client_id, session_id):
    """
    Description:
        This function will get the number of jobs left for a session
    Args:
        client_id (str): The client_id
        session_id (int): The session_id
    Returns:
        int: Simply an integer with count of jobs left zero otherwise
    Example Response:
        11
    """
    route = f"http://profgriffin.com:8000/jobsLeft?client_id={client_id}&session_id={session_id}"
    r = requests.get(route)
    if r.status_code == 200:
        response = r.json()
        return response
    else:
        print(f"Error: {r.status_code}")
        return None
