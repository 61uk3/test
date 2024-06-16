from typing import Annotated
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, File, Form
import json
from sqlalchemy.orm import Session
from fastapi import UploadFile
from database.PostgresDb import get_connection
from dto.User import  UpUser, AnswerUser
from models.Models import Users, Towns
from services import UsersService
from services.ItemService import get_items_by_user_id,add_photos_to_item
from services.ItemsPhotosService import get_first_photo_by_id
from services.MinioService import get_photo
from services.UsersService import get_current_user
router = APIRouter()
con_dependency = Annotated[Session, Depends(get_connection)]
@router.get('/{id}', tags=['user'])
async def get_user(con: con_dependency, id: UUID):
    items = await get_items_by_user_id(id, con)
    user = con.query(Users).filter(Users.id==id).first()
    photo = get_first_photo_by_id(user.id, con)
    f_p = str(photo.id_lots)
    s_p = str(photo.photo)
    photo_url = await get_photo(f"{f_p}/{s_p}")
    return AnswerUser(
        name=user.name,
        contact=user.contact,
        datereg=user.datereg,
        photo=photo_url,
        town= con.query(Towns).filter(user.id_town == Towns.id).scalar(),
        items=items
    )
@router.post('/{id}/photos', tags=['user'])
async def post_photos_for_item(
        con: con_dependency,
        id: UUID,
        photos: List[UploadFile] = File(...)
):
    await add_photos_to_item(con, id, photos)
    return {"message": "Photos added successfully"}
@router.post('/up/',tags=['user'])
async def update_inf(
        con: con_dependency,
        user_json: str = Form(...),
        town: str = Form(...),
        men: int = Form(...),
        user: Users = Depends(get_current_user)
):
    user_data = json.loads(user_json)
    user_new = UpUser(**user_data)
    return await UsersService.uppdate_user(con,user,user_new,town,men)
@router.get('/', tags=['user'])
async def get_user(con: con_dependency, user: Users = Depends(get_current_user)):
    items = await get_items_by_user_id(user.id, con)
    photo = get_first_photo_by_id(user.id, con)
    f_p = str(photo.id_lots)
    s_p = str(photo.photo)
    photo_url = await get_photo(f"{f_p}/{s_p}")
    return AnswerUser(
        name=user.name,
        contact=user.contact,
        datereg=user.datereg,
        photo=photo_url,
        town= con.query(Towns).filter(user.id_town == Towns.id).scalar(),
        items=items
    )