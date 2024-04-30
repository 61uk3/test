import json
import uuid
from typing import Annotated
from datetime import datetime
from fastapi import HTTPException, UploadFile
from fastapi import FastAPI, Form
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import dto.Photo
import services.ItemsPhotosService
from database.PostgresDb import get_connection
from dto.User import RegUser, UpUser
from models.Models import Users
from models.Models import Towns
from models.Models import Photos
from services.AuthService import verify_jwt_token
from services.MinioService import save_photo, delete_photos

# используется для получения токена доступа
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")
con_dependency = Annotated[Session, Depends(get_connection)]


async def register_user(user: RegUser,
                        town:str,
                        repository: Session) -> Users:

    uid = uuid.uuid1()
    townid = repository.query(Towns.id).filter(town == Towns.town).first()
    add_user = Users(
        id=uid,
        name=user.name,
        login=user.login,
        password=user.password,
        contact=user.contact,
        datereg=str(datetime.now())[:-7],
        id_town= townid
    )

    try:
        repository.add(add_user)
        repository.commit()

    except Exception as e:
        print(e)

    return add_user.id


def get_user_by_id(userId: str, repository: Session) -> type[Users] | None:
    user = repository.query(Users).filter(Users.id == userId).first()
    return user

def get_user_by_login(userLogin: str, repository: Session) -> type[Users] | None:
    user = repository.query(Users).filter(Users.login == userLogin).first()
    return user

def get_current_user(con: con_dependency, token: str = Depends(oauth2_scheme)):
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = get_user_by_id(decoded_data["sub"], con)  # Получите пользователя из базы данных
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user

async def uppdate_user(
        con:Session,
        user: Users,
        new_user:UpUser,
        town: str):
    try:

        # Обновление значений пользователя
        user.name = new_user.name
        user.contact = new_user.contact
        user.login = new_user.login

        town_id = con.query(Towns.id).filter(Towns.town == town).scalar()
        user.id_town = town_id

        con.query(Photos).filter(Photos.id_lots == user.id).delete()
        await delete_photos(user.id)


        con.commit()
        return user

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user: {e}")


