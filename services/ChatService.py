import uuid
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import pytz
from dto.Chat import ShortChat
from dto.Message import Shortmes
from dto.User import ChatWithUser
from models.Models import Items, Chats, Messages, Users
from services.ItemsPhotosService import get_first_photo_by_id
from services.MinioService import get_photo

async def get_chats(con:Session,
                    user: Users):
    user_chats = con.query(Chats).filter(or_(Chats.id_user1 == user.id, Chats.id_user2 == user.id)).all()
    chats_list = []
    for chat in user_chats:
        chat_id=chat.id
        last_message = con.query(Messages).filter(Messages.id_Chats == chat_id).order_by(Messages.date.desc()).first()
        lot_info = con.query(Items).filter(Items.id == chat.id_Lots).first()
        sender = con.query(Users.name).filter(last_message.id_sender == Users.id).scalar()
        photo = get_first_photo_by_id(lot_info.id, con)
        f_p = str(photo.id_lots)
        s_p = str(photo.photo)
        photo_url = await get_photo(f"{f_p}/{s_p}")
        try:
                short_chat = ShortChat(
                    id=chat.id,
                    photo_lots= photo_url,
                    name_lots=lot_info.name,
                    last_message=last_message.message,
                    date=str(last_message.date),
                    sender_name= sender
                )
                chats_list.append(short_chat)
        except Exception as e:
         raise HTTPException(status_code=500, detail=f"Failed to send message: {e}")
    return chats_list

async def createchat(con:Session,
               id1:UUID,
               id2:UUID,
               idl:UUID):
    chat = Chats(
        id=uuid.uuid1(),
        id_user1=id1,
        id_user2=id2,
        id_Lots=idl
    )
    con.add(chat)
    con.commit()
    return  chat

async def from_lot(con:Session,
                   lot_id:UUID,
                   user_id:UUID):
    item = con.query(Items).filter(Items.id == lot_id).first()
    user = con.query(Users).filter(Users.id == user_id).first()
    chats = con.query(Chats).filter(Chats.id_Lots == lot_id).all()
    chat = None
    for chat_ in chats:
        if chat_.id_user1==user_id:
            chat = chat_
    if chat == None:
            chat = await createchat(con, user_id, item.id_Users, lot_id)
    return await get_mes(con,chat.id,user)


async def send(con:Session,
                    chat_id:UUID,
                    message:str,
                    user_id: UUID):
    try:
        timezone = pytz.timezone('Europe/Moscow')
        utc_now = datetime.now(pytz.utc)
        local_now = str(utc_now.astimezone(timezone))[:-13]


        new_message = Messages(
                id=uuid.uuid1(),
                id_sender=user_id,
                date=local_now,
                message=message,
                id_Chats=chat_id
        )
        con.add(new_message)
        con.commit()
        return new_message
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message: {e}")

async def get_mes(
        con:Session,
        id_chat:UUID,
        user:Users):
    chat = con.query(Chats).filter(Chats.id == id_chat).first()
    user_info = con.query(Users).filter((Users.id == chat.id_user1) | (Users.id == chat.id_user2)).all()
    for us in user_info:
        if (us.id != user.id):
            another_user = us
    lot_info = con.query(Items).filter(Items.id == chat.id_Lots).first()
    userphoto = get_first_photo_by_id(another_user.id, con)
    user_photo= await get_photo(f"{userphoto.id_lots}/{userphoto.photo}")
    lotphoto = get_first_photo_by_id(lot_info.id, con)
    lot_photo = await get_photo(f"{lotphoto.id_lots}/{lotphoto.photo}")
    messages = con.query(Messages).filter(Messages.id_Chats == id_chat).order_by(Messages.date).all()
    messages_list = []
    for message in messages:
        message_data = Shortmes(
            id_sender=message.id_sender,
            date_send=str(message.date),
            message=message.message
        )
        messages_list.append(message_data)
    chat_with_user = ChatWithUser(
        id=chat.id,
        user_id=another_user.id,
        user_name=another_user.name,
        user_photo=user_photo,
        lot_id=lot_info.id,
        lot_photo=lot_photo,
        lot_name=lot_info.name,
        messages=messages_list
    )
    return chat_with_user

async def get_only_mes(
        con:Session,
        id_chat:UUID):
    messages = con.query(Messages).filter(Messages.id_Chats == id_chat).order_by(Messages.date).all()
    messages_list = []
    for message in messages:
        message_data = Shortmes(
            id_sender=message.id_sender,
            date_send=str(message.date),
            message=message.message
        )
        messages_list.append(message_data)
    return messages_list