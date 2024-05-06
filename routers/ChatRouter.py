from typing import Annotated, List
from uuid import UUID
import json
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status
from fastapi import File, UploadFile
import services.ItemService as ItemServices
from database.PostgresDb import get_connection
from dto import Item as ItemDto
from models.Models import Users
from services import ChatService
from services.UsersService import get_current_user
from typing import Dict, List

router = APIRouter()
con_dependency = Annotated[Session, Depends(get_connection)]

@router.get('/', tags=['chat'], response_model=None)
async def get_chats(con: con_dependency,
                    user: Users = Depends(get_current_user)):
    return await ChatService.get_chats(con, user)

@router.post('/{id}', tags=['chat'], response_model=None)
async def send_message(con: con_dependency,
                       id: UUID,
                       message: str = Form(...),
                       user: Users = Depends(get_current_user)):
    return await ChatService.send(con, id,message, user.id)


@router.get('/{id}', tags=['chat'], response_model=None)
async def get_chat_messages(
        con: con_dependency,
        id: UUID,
        user: Users = Depends(get_current_user)):
    return await ChatService.get_mes(con,id,user)

@router.post('/create/{id}', tags=['chat'], response_model=None)
async def send_message(con: con_dependency,
                       id: UUID,
                       user: Users = Depends(get_current_user)):
    return await ChatService.from_lot(con, id, user.id)

