from ..schemas import ShopModel
from ..app import api_router
from ..db import Session
from ..db.models import Shop

from fastapi import HTTPException,UploadFile, Form
from typing import Annotated
import os
import shutil
from sqlalchemy import func, or_

UPLOAD_FOLDER = './frontend/static/photos/uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@api_router.post("/shop/add_new_clothing")
def add_new_clothing(data:Annotated[ShopModel, Form(media_type="multipart/form-data")]):
    with Session() as session:
        shop = Shop(
            name=data.name,
            gender=data.gender,
            type_of_clothes=data.type_of_clothes,
            name_of_clothes=data.name_of_clothes,
            discount=data.discount,
            price=data.price,
            sizes = data.sizes,
            photo=data.photo.filename,
            description=data.description,
            styles=data.styles,
            model=data.model,
            created_at=data.created_at
        )
        last_id = session.query(func.max(Shop.id)).scalar()
        upload_path = ""
        if last_id == None:
            upload_path = os.path.join(UPLOAD_FOLDER, "1")
        else:
            upload_path = os.path.join(UPLOAD_FOLDER, str(last_id+1))

        os.makedirs(upload_path, exist_ok=True)
        photo_path = os.path.join(upload_path, data.photo.filename)

        with open(photo_path, "wb") as buffer:
            shutil.copyfileobj(data.photo.file, buffer)

        if data.photo_hover:
            shop.photo_hover=data.photo_hover.filename
            photo_hover_path = os.path.join(upload_path, data.photo_hover.filename)

            with open(photo_hover_path, "wb") as buffer:
                shutil.copyfileobj(data.photo_hover.file, buffer)
                
        if data.variable:
            shop.variable=data.variable.filename
            variable_path = os.path.join(upload_path, data.variable.filename)
            with open(variable_path, "wb") as buffer:
                shutil.copyfileobj(data.variable.file, buffer)

        photos = []

        if data.add_photos:
            for photo in data.add_photos:
                photo_path = os.path.join(upload_path, photo.filename)
                photos.append(photo.filename)
                with open(photo_path, "wb") as buffer:
                    shutil.copyfileobj(photo.file, buffer)

        shop.photos = photos
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
        
        path = os.path.join(UPLOAD_FOLDER, str(shop.id))

        if shop.photo:
            os.remove(os.path.join(path, shop.photo))
        if shop.photo_hover:
            os.remove(os.path.join(path, shop.photo_hover))
        if shop.variable:
            os.remove(os.path.join(path, shop.variable))
        if shop.photos:
            for i in shop.photos:
                os.remove(os.path.join(path, i))
        
        session.delete(shop)
        session.commit()

        return {"message": "Clothing is deleted"}
    

@api_router.put("/shop/{id}/change_clothing")
def change_clothing(id,data:Annotated[ShopModel, Form(media_type="multipart/form-data")]):
    with Session() as session:
        shop = session.query(Shop).where(Shop.id == id).first() 

        if not shop:
            raise HTTPException(404,"Clothing not found")
        
        shop.name = data.name
        shop.gender = data.gender
        shop.price = data.price
        shop.type_of_clothes = data.type_of_clothes
        shop.name_of_clothes = data.name_of_clothes
        shop.discount = data.discount
        shop.sizes = data.sizes
        shop.description = data.description
        shop.styles = data.styles
        shop.model = data.model
        
        path = os.path.join(UPLOAD_FOLDER,str(shop.id))
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except Exception as e:
                print(f"Cannot delete {item_path}. Error: {e}")

        if data.photo:
            photo_filename = data.photo.filename

            with open(path, "wb") as buffer:
                shutil.copyfileobj(data.photo.file, buffer)

            shop.photo = photo_filename
            
        if data.photo_hover:
            photo_hover_filename = data.photo_hover.filename

            with open(path, "wb") as buffer:
                shutil.copyfileobj(data.photo_hover.file, buffer)

            shop.photo_hover = photo_hover_filename
        
        if data.variable:
            variable_filename = data.variable.filename

            with open(path, "wb") as buffer:
                shutil.copyfileobj(data.variable.file, buffer)

            shop.photo_hover = variable_filename

        if data.add_photos:
            photos = []
            for i in data.add_photos:
                photo_filename = i.filename
                with open(path, "wb") as buffer:
                    shutil.copyfileobj(i.file, buffer)
                photos.append(photo_filename)
            shop.photos = photos


        session.commit()
        
        return shop
    

@api_router.get("/shop/get_all_clothing_by_type")
def get_all_clothing_by_type(type_of:str):
    with Session() as session:
        shop = session.query(Shop).where(Shop.name_of_clothes == type_of).all()
        if not shop:
            raise HTTPException(404,"Clothing not found") 
        return shop
    

@api_router.get("/shop/get_all_clothing_by_gender")
def get_all_clothing_by_type(gender:str):
    with Session() as session:
        shop = session.query(Shop).where(or_(Shop.gender == gender, Shop.gender == "Men's / Woman's")).all()
        if not shop:
            raise HTTPException(404,"Clothing not found") 
        return shop
    

@api_router.get("/shop/get_all_clothing")
def get_all_clothing():
    with Session() as session:
        shop = session.query(Shop).all()
        if not shop:
            raise HTTPException(404,"Clothing not found")
        return shop
    

@api_router.get("/shop/get_all_clothing_by_id")
def get_all_clothing_by_type(id:int):
    with Session() as session:
        shop = session.query(Shop).where(Shop.id == id).first()
        if not shop:
            raise HTTPException(404,"Clothing not found")
        return shop