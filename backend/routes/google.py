from fastapi import APIRouter,HTTPException
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from os import getenv
from dotenv import load_dotenv

load_dotenv()


oauth = OAuth()
google = oauth.register(
    name='google',
    client_id=getenv("CLIENT_ID"),
    client_secret=getenv("CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)


google_router = APIRouter(prefix="/google", tags=["Google"])

@google_router.get("/auth/login")
async def login_via_google(request: Request):
    redirect_uri = getenv("BACKEND_URL") + "/api/google/auth/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@google_router.get("/auth/callback")
async def auth_callback(request: Request):
    try:
        token = await google.authorize_access_token(request)
        user_info = token.get("userinfo")
        if user_info:
            return {"email": user_info["email"], "name": user_info["name"]}
        raise HTTPException(status_code=400, detail="Google login failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))