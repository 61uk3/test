from typing import Annotated
from uuid import UUID
import json
from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from fastapi import File, UploadFile
import services.ItemService as ItemServices
from database.PostgresDb import get_connection
from dto import Item as ItemDto
from models.Models import Users
from services.UsersService import get_current_user
from typing import List
router = APIRouter()
con_dependency = Annotated[Session, Depends(get_connection)]
@router.get('/', tags=['items'], response_model=None)
async def get_items(con: con_dependency,
                    user: Users = Depends(get_current_user)):
    return await ItemServices.get_items(user.id,con)
@router.get('/{id}', tags=['items'], response_model=None)
async def get_item_by_id(id: UUID, con: con_dependency):
    return await ItemServices.get_item_by_id(id, con)
@router.post('/', tags=['items'])
async def post_item(
        con: con_dependency,
        lot_json: str = Form(...),
        cat: str = Form(...),
        cond: str = Form(...),
        user: Users = Depends(get_current_user)
):
    lotdata = json.loads(lot_json)
    lot = ItemDto.InputItem(**lotdata)
    item_id = await ItemServices.create_item(con, lot, user.id, cat, cond)
    return item_id
@router.post('/{id}/photos', tags=['items'])
async def post_photos_for_item(
        id: UUID,
        con: con_dependency,
        photos: List[UploadFile] = File(...),
):
    await ItemServices.add_photos_to_item(con, id, photos)
    return {"message": "Photos added successfully"}
@router.get('/user/{id}', tags=['items'], response_model=None)
async def get_item_by_id_user(id: UUID, con: con_dependency):
    return await ItemServices.get_items_by_user_id(id, con)
@router.post('/up/{id}',tags=['items'])
async def update_item(
        con: con_dependency,
        id: UUID,
        lot_json: str = Form(...),
        photos: List[UploadFile] = File(None),
        cat: str = Form(...),
        cond: str = Form(...),
        men: int = Form(...)):
    lotdata = json.loads(lot_json)
    lot = ItemDto.InputItem(**lotdata)
    await ItemServices.update_item(con, id, lot, cat, cond, men)
    if (men == 1):
        await ItemServices.add_photos_to_item(con, id, photos)
    return {"message": "Item updated successfully"}
@router.post('/inactive/{id}',tags=['items'])
async def update_item(
        con: con_dependency,
        id: UUID
        ):
    await ItemServices.update_active(con, id)
    return {"message": "Active updated successfully"}
@router.delete('/{id}', tags=['items'])
async def delete_item(id: UUID, con: con_dependency, user: Users = Depends(get_current_user)):
    return await ItemServices.delete_item(id, con, user.id)
