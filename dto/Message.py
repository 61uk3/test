
from pydantic import BaseModel


class Message(BaseModel):
    id_отправителя:int
    Сообщение:str
    Дата: str



