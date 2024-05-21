import uuid
from uuid import UUID

from fastapi import HTTPException, UploadFile
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, List
from dto import Item as DtoItem
from dto.Item import CardItem, ShortItem

from models.Models import Items, Towns, Users
from models.Models import Photos
from models.Models import Categories, Conditions

from services.ItemsPhotosService import get_first_photo_by_id, get_all_photos_by_id
from services.MinioService import get_photo, save_photo, delete_photos
from services.UsersService import get_user_by_id



async def get_items(con: Session):
    answered_list = con.query(Items).filter(Items.active == True).all()
    ret_list = []
    for item in answered_list:
        photo = get_first_photo_by_id(item.id, con)
        f_p = str(photo.id_lots)
        s_p = str(photo.photo)
        photo_url = await get_photo(f"{f_p}/{s_p}")
        user = con.query(Users).filter(Items.id_Users==Users.id).first()
        town = str(con.query(Towns.town).filter(Towns.id == user.id_town).scalar())
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
    con.query(Items).filter(Items.id == id and Items.id_Users == userId).delete()
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
#06a514c4-ff25-11ee-8f6d-975f61d225b4
# elf.id = id
#         self.name = name
#         self.description = description
#         self. = date
#         self.categories = categories
#         self.conditions = conditions
#         self.photos = photos




# async def post_item(
#         lot: DtoItem.InputItem,
#         userId: UUID,
#         photo1: UploadFile,
#         photo2: UploadFile,
#         photo3: UploadFile,
#         photo4: UploadFile,
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
#         await save_photo(item_id, photo1)
#         con.add(Photos(
#             id=uuid.uuid1(),
#             photo=photo1.filename,
#             id_lots=item_id
#         ))
#
#         if photo2.size !=0:
#             await save_photo(item_id, photo2)
#             con.add(Photos(
#                 id=uuid.uuid1(),
#                 photo=photo2.filename,
#                 id_lots=item_id
#             ))
#
#             if photo3.size !=0:
#                 await save_photo(item_id, photo3)
#                 con.add(Photos(
#                     id=uuid.uuid1(),
#                     photo=photo3.filename,
#                     id_lots=item_id
#                 ))
#
#                 if photo4.size !=0:
#                     await save_photo(item_id, photo4)
#                     con.add(Photos(
#                         id=uuid.uuid1(),
#                         photo=photo4.filename,
#                         id_lots=item_id
#                     ))
#
#         con.commit()
#
#     except Exception as e:
#         print(e)
#
#     return item_id

# async def post_item_with_retry(
#     lot: DtoItem.InputItem,
#     userId: UUID,
#     photos: List[UploadFile],
#     cat: str,
#     cond: str,
#     con: Session,
#     max_retries: int = 5
# ):
#     for retry in range(max_retries):
#         try:
#             item_id = uuid.uuid1()
#             id_cat_subquery = select([Categories.id]).where(cat == Categories.category).scalar_subquery()
#             id_con_subquery = select([Conditions.id]).where(cond == Conditions.condition).scalar_subquery()
#             idcat = con.query(id_cat_subquery).scalar()
#             idcon = con.query(id_con_subquery).scalar()
#             item = Items(
#                 id=item_id,
#                 name=lot.name,
#                 active=True,
#                 description=lot.description,
#                 date=datetime.now(),
#                 address=lot.address,
#                 id_Users=userId,
#                 id_cat = idcat,
#                 id_con = idcon
#             )
#
#             con.add(item)
#
#             for photo in photos:
#                 await save_photo(item_id, photo)
#                 con.add(Photos(
#                     id=uuid.uuid1(),
#                     photo=photo.filename,
#                     id_lots=item_id
#                 ))
#             con.commit()
#             # Если удалось успешно сохранить, выходим из цикла
#             break
#
#         except Exception as e:
#             print(f"Error occurred on attempt {retry + 1}: {e}")
#             # Если это последняя попытка, поднимаем исключение
#             if retry == max_retries - 1:
#                 raise HTTPException(status_code=500, detail="Failed to post item after multiple retries")

async def create_item(con: Session, lot: DtoItem.InputItem, user_id: UUID, cat: str, cond: str):
    try:
        item_id = uuid.uuid1()
        #repository.query(Towns.id).filter(town == Towns.town)
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


async def update_item(con: Session, item_id: UUID, lot: DtoItem.InputItem, cat: str, cond: str):
    try:
        item = con.query(Items).filter(Items.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")

        # Обновление значений лота
        item.name = lot.name
        item.description = lot.description
        item.address = lot.address

        # Обновление категории и условия
        idcat = con.query(Categories.id).filter(cat == Categories.category).scalar()
        idcon = con.query(Conditions.id).filter(cond == Conditions.condition).scalar()

        item.id_Categories = idcat
        item.id_Conditions = idcon

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

