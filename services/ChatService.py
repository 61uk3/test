import uuid
from uuid import UUID

from fastapi import HTTPException, UploadFile
from sqlalchemy import func, select, or_
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, List
from dto import Item as DtoItem
from dto.Chat import ShortChat
from dto.Item import CardItem, ShortItem
from dto.Message import Shortmes
from dto.User import ChatWithUser

from models.Models import Items, Chats, Messages, Users
from models.Models import Photos
from models.Models import Categories, Conditions

from services.ItemsPhotosService import get_first_photo_by_id, get_all_photos_by_id
from services.MinioService import get_photo, save_photo, delete_photos
from services.UsersService import get_user_by_id

async def get_chats(con:Session,
                    user: Users):
    user_chats = con.query(Chats).filter(or_(Chats.id_user1 == user.id, Chats.id_user2 == user.id)).all()
    # Создаем список для хранения объектов ShortChat
    chats_list = []
    # Для каждого чата в списке user_chats
    for chat in user_chats:
        # Получаем последнее сообщение в чате
        chat_id=chat.id
        last_message = con.query(Messages).filter(Messages.id_Chats == chat_id).order_by(Messages.date.desc()).first()

        # Получаем информацию о лоте
        lot_info = con.query(Items).filter(Items.id == chat.id_Lots).first()
        sender = con.query(Users.name).filter(last_message.id_sender == Users.id).scalar()

        photo = get_first_photo_by_id(lot_info.id, con)
        f_p = str(photo.id_lots)
        s_p = str(photo.photo)
        photo_url = await get_photo(f"{f_p}/{s_p}")
        try:
            # Создаем объект ShortChat
                short_chat = ShortChat(
                    id=chat.id,
                    photo_lots= photo_url,
                    name_lots=lot_info.name,
                    last_message=last_message.message,
                    date=str(last_message.date),
                    sender_name= sender
                )

                # Добавляем short_chat в список
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
                    lot_id:UUID,
                    message:str,
                    user_id: UUID):
    try:
        item = con.query(Items).filter(Items.id == lot_id).first()
        user = con.query(Users).filter(Users.id == user_id).first()
        # Проверить, существует ли чат для данного лота
        if con.query(Chats).filter(Chats.id_Lots == lot_id and Chats.id_user1 == user_id).first():
            chat = con.query(Chats).filter(Chats.id_Lots == lot_id and Chats.id_user1 == user_id).first()
        else:
            chat = await createchat(con,user.id,item.id_Users,lot_id)

        # Создать новое сообщение
        new_message = Messages(
                id=uuid.uuid1(),
                id_sender=user.id,
                date=str(datetime.now())[:-7],
                message=message,
                id_Chats=chat.id
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