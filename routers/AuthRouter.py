import json
from typing import Annotated
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Form, HTTPException
import services.UsersService as UserService
from database.PostgresDb import get_connection
from dto.User import AuthUser, RegUser
from models.Models import Users
from services.AuthenticationService import *
router = APIRouter()
con_dependency = Annotated[Session, Depends(get_connection)]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
@router.post('/password')
async def update_pas(
        con: con_dependency,
        user: Users = Depends(UserService.get_current_user),
        old_pass : str = Form(...),
        new_pass: str = Form(...)
):
    if pwd_context.verify(old_pass, user.password):
        new_hashed_password = pwd_context.hash(new_pass)
        user.password = new_hashed_password
        con.commit()
        return True
    else:
        return False
@router.post('/register')
async def register_user(con: con_dependency,
                        user_json: str = Form(...),
                        town:str = Form(...)
                        ):
    user_data = json.loads(user_json)
    user = RegUser(**user_data)
    user.password = pwd_context.hash(user.password)
    return await UserService.register_user(user,town, con)
@router.post('/auth')
def authenticate_user(user: AuthUser, con: con_dependency):
    password = user.password
    user_login = user.login
    user_in_base = UserService.get_user_by_login(user_login, con)
    if not user_in_base:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    is_password_correct = pwd_context.verify(password, user_in_base.password)
    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    jwt_token = create_jwt_token({"sub": str(user_in_base.id)})
    return {"access_token": jwt_token, "token_type": "bearer"}
