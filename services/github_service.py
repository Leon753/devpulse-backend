import requests

def fetch_github_activity(username, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"https://api.github.com/users/{username}/events", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    return {"error": "Unable to fetch GitHub activity"}
