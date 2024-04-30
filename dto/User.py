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
    login: str
    contact: str

class ChatWithUser(BaseModel):
    user_id: uuid.UUID
    user_name: str
    user_photo: str
    lot_id: uuid.UUID
    lot_photo: str
    lot_name: str
    messages: list[Shortmes]


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

