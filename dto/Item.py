from uuid import UUID

from pydantic import BaseModel

from dto import User
from dto.Photo import Photo as Photo


class InputItem(BaseModel):
    name: str
    description: str
    address: str

 #    id = Column(UUID, primary_key=True,index=True)
 #    name = Column(String)
 #    active = Column(BOOLEAN)
 #    description = Column(String)
 #    date = Column(Date)
 #    id_Users = Column(UUID,ForeignKey("users.id"))
 #    id_Categories = Column(UUID,ForeignKey("categories.id"))
 #    id_Conditions = Column(UUID,ForeignKey("conditions.id"))
 #
 #    user = relationship('Users', back_populates='items')
 #    photo

class CardItem:
    id: UUID
    name: str
    description: str
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
        self.date = date
        self.condition = condition
        self.category = category
        self.user_name = user_name
        self.user_id = user_id
        self.photos = photos


class ShortItem:
    id: UUID
    name: str
    photo: str | None

    def __init__(self, id: UUID, name: str, photo: str | None):
        self.id = id
        self.name = name
        self.photo = photo
