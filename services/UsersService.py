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
from services.AuthenticationService import verify_jwt_token
from services.MinioService import delete_photos

# используется для получения токена доступа
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")
con_dependency = Annotated[Session, Depends(get_connection)]


async def register_user(user: RegUser,
                        town:str,
                        con: Session) -> Users:

    uid = uuid.uuid1()
    if (con.query(Users.login).filter(user.login==Users.login).first()) != None:
        return "login"
    if (con.query(Users.contact).filter(user.contact==Users.contact).first()) != None:
        return "contact"
    townid = str(con.query(Towns.id).filter(town == Towns.town).first())
    add_user = Users(
        id=uid,
        name=user.name,
        login=user.login,
        password=user.password,
        contact=user.contact,
        id_town=townid[townid.find("'") + 1:townid.rfind("'")],
        datereg=str(datetime.now().date())

    )

    try:
        con.add(add_user)
        con.commit()
        return add_user.id


    except Exception as e:

        con.rollback()

        raise HTTPException(status_code=500, detail=f"Failed to register user: {e}")


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
        town: str,
        men:int):
    try:

        user.name = new_user.name
        user.contact = new_user.contact

        town_id = con.query(Towns.id).filter(Towns.town == town).scalar()
        user.id_town = town_id

        if (men==1):
            con.query(Photos).filter(Photos.id_lots == user.id).delete()
            await delete_photos(user.id)


        con.commit()
        return user.id

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user: {e}")


