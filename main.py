from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routes import auth_routes, user_routes
from auth.oauth import oauth
from starlette.middleware.sessions import SessionMiddleware
from services.github_service import fetch_github_activity
import os

origins = [
    "http://localhost:3000", 
    "https://devpulse.duckdns.org",  
]


app = FastAPI(title="DevPulse API", description="GitHub Activity Tracker", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "supersecretkey"))
app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(user_routes.router, prefix="/github", tags=["GitHub"])

@app.get("/")
async def root():
    return {"message": "API is running"}
