import uuid

from pydantic import BaseModel

# from dto.Item import ShortItem
from dto.Chat import ShortChat


class RegUser(BaseModel):
    login: str
    name: str
    password: str
    contact: str

class AuthUser(BaseModel):
    login: str
    password: str


# class ResponseUser:
#     login: str
#     photo: str
#     name: str
#     password: str
#     contact: str
#     datereg: str
#     id_town: uuid
#     #items: list[ShortItem]
#     #chats: list[ShortChat]
#
#     def __init__(self,
#     login: str,
#     photo: str,
#     name: str,
#     password: str,
#     contact: str,
#     datereg: str,
#     id_town: uuid,
#     items: list[ShortItem]):
#         #,
#     #chats: list[ShortChat]
#         self.login =login
#         self.photo=photo
#         self.name=name
#         self.password=password
#         self.contact=contact
#         self.datereg=datereg
#         self.id_town=id_town
#         self.items=items
#         #self.chats=chats

