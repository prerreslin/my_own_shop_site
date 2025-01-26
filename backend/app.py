from fastapi import FastAPI,APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .routes import user_router, shop_router, giftcard_router

app = FastAPI()

api_router = APIRouter(prefix="/api")

api_router.include_router(user_router)
api_router.include_router(shop_router)
api_router.include_router(giftcard_router)
app.include_router(api_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from . import routes