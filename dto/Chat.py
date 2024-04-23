from pydantic import BaseModel


class ShortChat(BaseModel):
    id_чата: int
    id_пользователя1: int
    id_пользователя2: int
    id_лота_Лоты: int



