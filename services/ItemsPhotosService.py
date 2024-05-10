from typing import Type
from uuid import UUID

from sqlalchemy.orm import Session

from dto.Photo import Photo
from models.Models import Photos
from services.MinioService import get_photo


async def get_all_photos_by_id(id: UUID, con: Session) -> list[Photo]:
    list_photos = con.query(Photos).filter(Photos.id_lots == id).all()
    res_list = []
    for item in list_photos:
        photo_url = await get_photo(f"{item.id_lots}/{item.photo}")
        res_list.append(Photo(id=item.id, photo=photo_url))

    return res_list


def get_first_photo_by_id(id: UUID, con: Session) -> Type[Photos] | None:
    photo = con.query(Photos).filter(Photos.id_lots == id).first()
    return photo
