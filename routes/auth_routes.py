from fastapi import APIRouter, Request, Header, HTTPException
from auth.oauth import oauth
from starlette.responses import JSONResponse
from starlette.responses import RedirectResponse
import os
import requests

router = APIRouter()

EC2_IP = os.getenv("EC2_IP")

@router.get("/login")
async def login(request: Request):
    return await oauth.github.authorize_redirect(request, f"http://{EC2_IP}/auth/callback")

@router.get("/callback")
async def auth_callback(request: Request):
    token = await oauth.github.authorize_access_token(request)
    user = await oauth.github.get("https://api.github.com/user", token=token)

    response = RedirectResponse(url=f"https://{EC2_IP}") 
    response.set_cookie(
        key="oauth_token",
        value=token["access_token"],
        httponly=True, 
        secure=True,   # Use False for local development (change to True after deploying)
        samesite="None",
        max_age=3600
    )
    print("Set-Cookie Header:", response.headers.get("Set-Cookie"))
    return response

@router.get("/user")
async def get_user(request: Request):
    print("Incoming Request Headers:", request.headers)
    print("Incoming Request Cookies:", request.cookies)

    token = request.cookies.get("oauth_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not logged in - No token found")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://api.github.com/user", headers=headers)

    if response.status_code != 200: raise HTTPException(status_code=401, detail="Invalid token")

    return {"user": response.json()}
