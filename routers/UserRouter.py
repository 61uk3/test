from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi import APIRouter, Depends, File, Form, HTTPException
import json
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from database.PostgresDb import get_connection
from dto.User import ResponseUser, UpUser
from models.Models import Users, Towns
from services import UsersService
from services.ItemService import get_items_by_user_id,add_photos_to_item
from services.UsersService import get_current_user

router = APIRouter()
con_dependency = Annotated[Session, Depends(get_connection)]


@router.get('/{id}', tags=['user'])
async def get_user(con: con_dependency, id: UUID):
    items = await get_items_by_user_id(id, con)
    user = con.query(Users).filter(Users.id==id).first()
    return ResponseUser(
        name=user.name,
        contact=user.contact,
        datereg=user.datereg,
        photo=user.photo,
        town= con.query(Towns).filter(user.id_town == Towns.id).scalar(),
        items=items
    )

@router.put('',tags=['user'])
async def update_inf(
        con: con_dependency,
        user_json: str = Form(...),
        town: str = Form(...),
        user: Users = Depends(get_current_user)
):
    user_data = json.loads(user_json)
    user_new = UpUser(**user_data)
    return await UsersService.uppdate_user(con,user,user_new,town)

@router.put('/photo/{id}', tags=['user'])
async def update_photo(
        con: con_dependency,
        id: UUID,
        photo:list[UploadFile]=Form(...)
):
    return  await add_photos_to_item(con, id, photo)

    # /@router.put('/{id}',tags=['items'])
    # user_data = json.loads(user_json)
    # user = RegUser(**user_data)
    # user.password = pwd_context.hash(user.password)
    # return await UserService.register_user(user, town, photo, con)
# async def update_item(
#         con: con_dependency,
#         id: UUID,
#         lot_json: str = Form(...),
#         photos: List[UploadFile] = File(...),
#         cat: str = Form(...),
#         cond: str = Form(...)):
#     lotdata = json.loads(lot_json)
#     lot = ItemDto.InputItem(**lotdata)
#     await ItemServices.update_item(con, id, lot, cat, cond)
#     # Добавление новых фотографий
#     await ItemServices.add_photos_to_item(con, id, photos)
#
#     return {"message": "Item updated successfully"}