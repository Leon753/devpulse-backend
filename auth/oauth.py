from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv 
import os

load_dotenv()

oauth = OAuth()

client_id = os.getenv("GITHUB_CLIENT_ID")
client_secret = os.getenv("GITHUB_CLIENT_SECRET")

oauth.register(
    name="github",
    client_id=client_id,
    client_secret=client_secret,
    authorize_url="https://github.com/login/oauth/authorize",
    access_token_url="https://github.com/login/oauth/access_token",
    client_kwargs={"scope": "read:user"},
)
