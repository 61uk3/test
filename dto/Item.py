from uuid import UUID

from pydantic import BaseModel


from dto.Photo import Photo as Photo


class InputItem(BaseModel):
    name: str
    description: str
    address: str

class ShortItem:
    id: UUID
    name: str
    photo: str
    town : str
    condition: str
    category: str

    def __init__(self, id: UUID, name: str, photo: str, town:str,condition: str,category: str):
        self.id = id
        self.name = name
        self.photo = photo
        self.town = town
        self.condition=condition
        self.category=category


class CardItem:
    id: UUID
    name: str
    description: str
    address: str
    date: str
    category: str
    condition: str
    user_name: str
    user_id:UUID
    photos: list[Photo]

    def __init__(
                self,
                id: UUID,
                name: str,
                description: str,
                address: str,
                date: str,
                category: str,
                condition: str,
                user_name: str,
                user_id: UUID,
                photos: list[Photo]
    ):
        self.id = id
        self.name = name
        self.description = description
        self.address = address
        self.date = date
        self.condition = condition
        self.category = category
        self.user_name = user_name
        self.user_id = user_id
        self.photos = photos

