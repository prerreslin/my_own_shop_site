from ..db import Session
from ..db.models import Gift_Card
from ..schemas import GiftCardModel
from fastapi import HTTPException, APIRouter, Form
from typing import Annotated
from sqlalchemy.sql import func
import os
import shutil

giftcard_router = APIRouter(prefix="/gift_cards", tags=["Gift Cards"])
UPLOAD_FOLDER = './frontend/static/photos/uploads/gift_cards'

@giftcard_router.post("/add_card")
def add_new_clothing(data:Annotated[GiftCardModel, Form(media_type="multipart/form-data")]):
    with Session() as session:
        card = session.query(Gift_Card).where(Gift_Card.name == data.name).first()

        if card:
            raise HTTPException(409,"Card already exists")
        
        card = Gift_Card(
            name=data.name,
            description=data.description,
            description2=data.description2,
            price=data.price,
            photo=data.photo.filename
        )

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        photo_path = os.path.join(UPLOAD_FOLDER, data.photo.filename)

        with open(photo_path, "wb") as buffer:
            shutil.copyfileobj(data.photo.file, buffer)

        session.add(card)
        session.commit()
        session.refresh(card)

        return card
    

@giftcard_router.get("/get_all")
def get_all_cards():
    with Session() as session:
        cards = session.query(Gift_Card).all()
        return cards
    

@giftcard_router.get("/get_by_id")
def get_card_by_id(id:int):
    with Session() as session:
        card = session.query(Gift_Card).where(Gift_Card.id == id).first()
        if not card:
            raise HTTPException(404, "Card not found")
        return card
    

@giftcard_router.delete("/delete_card")
def delete_card(id:int):
    with Session() as session:
        card = session.query(Gift_Card).where(Gift_Card.id == id).first()
        if not card:
            raise HTTPException(404, "Card not found")
        session.delete(card)
        session.commit()
        return {"message":"Card deleted"}


@giftcard_router.delete("/delete_all")
def delete_all_cards():
    with Session() as session:
        session.query(Gift_Card).delete()
        session.commit()
        return {"message":"All cards deleted"}