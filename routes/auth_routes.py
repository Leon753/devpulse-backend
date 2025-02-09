from fastapi import APIRouter, Request
from auth.oauth import oauth
import os

router = APIRouter()

EC2_IP = os.getenv("EC2_IP")

@router.get("/login")
async def login(request: Request):
    return await oauth.github.authorize_redirect(request, f"http://{EC2_IP}/auth/callback")

@router.get("/callback")
async def auth_callback(request: Request):
    token = await oauth.github.authorize_access_token(request)
    user = await oauth.github.get("https://api.github.com/user", token=token)

    # Store user info & token in session (or a database)
    request.session["user"] = user.json()
    request.session["token"] = token["access_token"]

    return {"message": "Authentication successful", "user": user.json()}
