# from typing import Annotated
#
# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
#
# from database.PostgresDb import get_connection
# from dto.User import ResponseUser
# from models.Models import Users
# from services.ItemService import get_items_by_userid
# from services.UsersService import get_current_user
#
# router = APIRouter()
# con_dependency = Annotated[Session, Depends(get_connection)]
#
#
# @router.get('/', tags=['user'])
# async def get_user(con: con_dependency, user: Users = Depends(get_current_user)):
#     items = await get_items_by_userid(user.id, con)
#     return ResponseUser(
#         login=user.login,
#         fullname=user.fullname,
#         items=items
#     )
#
