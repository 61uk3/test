from uuid import UUID
from pydantic import BaseModel
class Shortmes(BaseModel):
    id_sender: UUID
    date_send: str
    message:str