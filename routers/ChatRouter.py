from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from database.PostgresDb import get_connection
from models.Models import Users
from services import ChatService
from services.UsersService import get_current_user
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
@router.get('/mes/{id}', tags=['chat'], response_model=None)
async def get_chat_messages(
        con: con_dependency,
        id: UUID):
    return await ChatService.get_only_mes(con,id)
@router.post('/create/{id}', tags=['chat'], response_model=None)
async def send_message(con: con_dependency,
                       id: UUID,
                       user: Users = Depends(get_current_user)):
    return await ChatService.from_lot(con, id, user.id)

