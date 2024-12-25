from ..schemas import ShopModel
from ..app import api_router
from ..db import Session
from ..db.models import Shop

from fastapi import HTTPException,UploadFile, Form
from typing import Annotated
import os
import shutil

UPLOAD_FOLDER = './uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@api_router.post("/shop/add_new_clothing")
def add_new_clothing(data:Annotated[ShopModel, Form(media_type="multipart/form-data")]):
    with Session() as session:
        shop = Shop(
            name=data.name,
            description=data.description,
            price=data.price,
            photo=data.photo.filename,
            created_at=data.created_at
        )

        photo_path = os.path.join(UPLOAD_FOLDER, data.photo.filename)

        with open(photo_path, "wb") as buffer:
            shutil.copyfileobj(data.photo.file, buffer)

        session.add(shop)
        session.commit()
        session.refresh(shop)

        return shop

    


@api_router.delete("/shop/{id}/remove_clothing")
def remove_clothing(id):
    with Session() as session:
        shop = session.query(Shop).filter(Shop.id == id).first()

        if not shop:
            raise HTTPException(status_code=404, detail="Clothing not found")

        if shop.photo:
            os.remove(os.path.join(UPLOAD_FOLDER, shop.photo))

        session.delete(shop)
        session.commit()

        return {"message": "Clothing is deleted"}
    

@api_router.put("/shop/{id}/change_clothing")
def change_clothing(id,data:ShopModel,photo:UploadFile):
    with Session() as session:
        shop = session.query(Shop).where(Shop.id == id).first() 

        if not shop:
            raise HTTPException(404,"Clothing not found")
        
        shop.name = data.name
        shop.description = data.description
        shop.price = data.price
        
        if photo:
            photo_filename = photo.filename
            photo_path = os.path.join(UPLOAD_FOLDER)

            with open(photo_path, "wb") as buffer:
                shutil.copyfileobj(photo.file, buffer)

            shop.photo = photo_filename

        session.commit()
        
        return shop
    

@api_router.get("/shop/{id}/get_clothing")
def get_clothing(id):
    with Session() as session:
        shop = session.query(Shop).where(Shop.id == id).first() 

        if not shop:
            raise HTTPException(404,"Clothing not found")
        
        return shop