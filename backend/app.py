from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from os import getenv
from dotenv import load_dotenv
from .routes import user_router, shop_router, giftcard_router, google_router

load_dotenv()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://db07-188-163-95-216.ngrok-free.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=getenv("SECRET_KEY"))

api_router = APIRouter(prefix="/api")

api_router.include_router(user_router)
api_router.include_router(shop_router)
api_router.include_router(giftcard_router)
api_router.include_router(google_router)

app.include_router(api_router)


from . import routes