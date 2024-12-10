import requests

base_url ="http://localhost:8080/"

def call_api(endpoint, method="get", params=None, data=None):
    url = f"{base_url}{endpoint}"
    # headers = {"Content-Type": "application/json"}

    try:
        if method.lower() == "get":
            response = requests.get(url, params=params)
        elif method.lower() == "post":
            response = requests.post(url, json=data)
        elif method.lower() == "put":
            response = requests.put(url, json=data)
        elif method.lower() == "delete":
            response = requests.delete(url, json=data)
        else:
            raise ValueError("Unsupported HTTP method")

        # Handle response status
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            return

    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return
