import uuid

from pydantic import BaseModel
from dto.Item import ShortItem
from dto.Message import Shortmes


class RegUser(BaseModel):
    login: str
    name: str
    password: str
    contact: str

class AuthUser(BaseModel):
    login: str
    password: str

class UpUser(BaseModel):
    name: str
    contact: str

class ChatWithUser(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    user_name: str
    user_photo: str
    lot_id: uuid.UUID
    lot_photo: str
    lot_name: str
    messages: list[Shortmes]

class AnswerUser:
    login: str
    name: str
    password: str
    contact: str
    datereg: str
    id_town: uuid
    photo: str
    items: list[ShortItem]

    def __init__(self,
    name: str,
    contact: str,
    datereg: str,
    town: str,
    photo:str,
    items: list[ShortItem]):
        self.name=name
        self.contact=contact
        self.datereg=datereg
        self.town=town
        self.photo=photo
        self.items=items

class ResponseUser:
    login: str
    name: str
    password: str
    contact: str
    datereg: str
    id_town: uuid
    items: list[ShortItem]

    def __init__(self,
    name: str,
    contact: str,
    datereg: str,
    town: str,
    items: list[ShortItem]):
        self.name=name
        self.contact=contact
        self.datereg=datereg
        self.town=town
        self.items=items

