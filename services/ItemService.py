import uuid
from uuid import UUID
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from dto import Item as DtoItem
from dto.Item import CardItem, ShortItem
from models.Models import Items, Towns, Users
from models.Models import Photos
from models.Models import Categories, Conditions
from services.ItemsPhotosService import get_first_photo_by_id, get_all_photos_by_id
from services.MinioService import get_photo, save_photo, delete_photos
from services.UsersService import get_user_by_id
async def get_items(id: UUID,
                    con: Session):
    answered_list = con.query(Items).filter(Items.active == True).all()
    ret_list = []
    for item in answered_list:
        if item.id_Users != id:
            photo = get_first_photo_by_id(item.id, con)
            f_p = str(photo.id_lots)
            s_p = str(photo.photo)
            photo_url = await get_photo(f"{f_p}/{s_p}")
            user =  con.query(Users).filter(item.id_Users == Users.id).first()
            town =  str(con.query(Towns.town).filter(Towns.id == user.id_town).scalar())
            cond =  str(con.query(Conditions.condition).filter(Conditions.id==item.id_Conditions).scalar())
            cat =  str(con.query(Categories.category).filter(Categories.id == item.id_Categories).scalar())
            ret_list.append(
                ShortItem(
                    id=item.id,
                    name=item.name,
                    photo=photo_url,
                    town=town,
                    condition=cond,
                    category=cat))
    return ret_list
async def get_items_by_user_id(userId: UUID, con: Session):
    answered_list = con.query(Items).filter(Items.id_Users == userId).all()
    ret_list = []
    for item in answered_list:
        photo = get_first_photo_by_id(item.id, con)
        photo_url = await get_photo(f"{photo.id_lots}/{photo.photo}")

        user = con.query(Users).filter(Items.id_Users == userId).first()
        town = str(con.query(Towns.town).filter(Towns.id == user.id_town).scalar())
        cond = str(con.query(Conditions.condition).filter(Conditions.id == item.id_Conditions).scalar())
        cat = str(con.query(Categories.category).filter(Categories.id == item.id_Categories).scalar())
        ret_list.append(
            ShortItem(
                id=item.id,
                name=item.name,
                photo=photo_url,
                town=town,
                condition=cond,
                category=cat))
    return ret_list
async def delete_item(id: UUID, con: Session, userId: UUID):
    con.query(Items).filter(Items.id == id, Items.id_Users == userId).delete()
    con.query(Photos).filter(Photos.id_lots == id).delete()
    con.commit()
    await delete_photos(id)
async def get_item_by_id(id: UUID, con: Session):
    item = con.query(Items).filter(Items.id == id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    list_photos = await get_all_photos_by_id(id, con)
    name = get_user_by_id(item.id_Users, con).name
    user= get_user_by_id(item.id_Users, con)
    town = con.query(Towns.town).filter(Towns.id == user.id_town).first()[0]
    cond_k = con.query(Conditions.condition).filter(item.id_Conditions == Conditions.id).first()
    cat_k = con.query(Categories.category).filter(item.id_Categories == Categories.id).first()
    cond = cond_k[0]
    cat = cat_k[0]
    return CardItem(
        id=item.id,
        name=item.name,
        description=item.description,
        address = town +", " + item.address,
        date=str(item.date),
        category=cat,
        condition=cond,
        user_name=name,
        user_id=user.id,
        photos=list_photos
    )
async def create_item(con: Session, lot: DtoItem.InputItem, user_id: UUID, cat: str, cond: str):
    try:
        item_id = uuid.uuid1()
        idcat = con.query(Categories.id).filter(cat == Categories.category).scalar()
        idcon = con.query(Conditions.id).filter(cond == Conditions.condition).scalar()
        item = Items(
            id=item_id,
            name=lot.name,
            active=True,
            description=lot.description,
            date=datetime.now(),
            address=lot.address,
            id_Users=user_id,
            id_Categories=idcat,
            id_Conditions=idcon
        )
        con.add(item)
        con.commit()
        return item_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create item: {e}")
async def update_active(con: Session, item_id: UUID):
    try:
        item = con.query(Items).filter(Items.id == item_id).first()
        if item.active:
            item.active = False
        else:
             item.active = True
        con.commit()
        return item.active
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update item: {e}")
async def update_item(con: Session, item_id: UUID, lot: DtoItem.InputItem, cat: str, cond: str, men: int):
    try:
        item = con.query(Items).filter(Items.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        item.name = lot.name
        item.description = lot.description
        item.address = lot.address
        idcat = con.query(Categories.id).filter(cat == Categories.category).scalar()
        idcon = con.query(Conditions.id).filter(cond == Conditions.condition).scalar()
        item.id_Categories = idcat
        item.id_Conditions = idcon
        if (men==1):
            con.query(Photos).filter(Photos.id_lots == item_id).delete()
            await delete_photos(item_id)
        con.commit()
        return item_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update item: {e}")
async def add_photos_to_item(con: Session, id: UUID, photos: List[UploadFile]):
    try:
        for photo in photos:
            await save_photo(id, photo)
            con.add(Photos(
                id=uuid.uuid1(),
                photo=photo.filename,
                id_lots=id
            ))
        con.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add photos to item: {e}")
        print(e)



# async def post_item(
#         lot: DtoItem.InputItem,
#         userId: UUID,
#         photos: List[UploadFile],
#         cat: str,
#         cond: str,
#         con: Session):
#
#
#     item_id = uuid.uuid1()
#     id_cat = con.query(Categories.id).filter(cat == Categories.category)
#     id_con = con.query(Conditions.id).filter(cond == Conditions.condition)
#     item = Items(
#         id=item_id,
#         name=lot.name,
#         active=True,
#         description=lot.description,
#         date=datetime.now(),
#         address=lot.address,
#         id_Users=userId,
#         id_Categories=id_cat,
#         id_Conditions=id_con
#     )
#
#     con.add(item)
#
#     try:
#         for photo in photos:
#             await save_photo(item_id, photo)
#             con.add(Photos(
#                 id=uuid.uuid1(),
#                 photo=photo.filename,
#                 id_lots=item_id
#             ))
#         con.commit()
#
#     except Exception as e:

