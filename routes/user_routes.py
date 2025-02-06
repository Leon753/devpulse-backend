from fastapi import APIRouter, Depends, Request
from auth.dependencies import get_current_user  # Ensure user is authenticated
import httpx

router = APIRouter()

@router.get("/repos")
async def get_repos(request: Request, user: dict = Depends(get_current_user)):
    token = request.session.get("token")
    if not token:
        return {"error": "Unauthorized"}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user/repos?visibility=public",
            headers={"Authorization": f"Bearer {token}"}
        )
    return response.json()

@router.get("/activity")
async def get_github_activity(request: Request):
    token = request.session.get("token")
    user = request.session.get("user")

    if not token or not user:
        return {"error": "Unauthorized"}

    username = user["login"]

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/users/{username}/events",
            headers={"Authorization": f"Bearer {token}"}
        )

    events = response.json()

    # Format the data for frontend consumption
    activity_summary = {
        "commits": sum(1 for event in events if event["type"] == "PushEvent"),
        "pull_requests": sum(1 for event in events if event["type"] == "PullRequestEvent"),
        "issues": sum(1 for event in events if event["type"] == "IssuesEvent"),
        "events": [
            {
                "type": event["type"],
                "repo": event["repo"]["name"],
                "created_at": event["created_at"]
            }
            for event in events
            if event["type"] in ["PushEvent", "PullRequestEvent", "IssuesEvent"]
        ]
    }

    return activity_summary  # ✅ Now returns structured data
