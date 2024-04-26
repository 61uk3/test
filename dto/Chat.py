import datetime

from uuid import UUID

from pydantic import BaseModel


class ShortChat:
    id: UUID
    photo_lots:str
    name_lots:str
    last_message:str
    date:str
    sender_name:str

    def __init__(self,
                 id: UUID,
                 photo_lots: str,
                 name_lots: str,
                 last_message: str,
                 date: str,
                 sender_name: str
                 ):
        self.id=id
        self.photo_lots=photo_lots
        self.name_lots=name_lots
        self.last_message=last_message
        self.date = date
        self.sender_name=sender_name



