import os
from uuid import UUID

from fastapi import UploadFile
from miniopy_async import Minio

# Имя бакета в MinIO, куда будут загружаться фотографии и откуда будут получаться и удаляться
BUCKET_NAME = "photos"

# Создание экземпляра клиента MinIO с использованием информации об URL MinIO,
# ключе доступа и секретном ключе, полученных из переменных окружения
client = Minio(
    os.getenv("MINIO_URL"),
    access_key=os.getenv('MINIO_ACCESS_KEY'),
    secret_key=os.getenv('MINIO_SECRET_KEY'),
    secure=False
)


# Функция для получения фотографии с заданным именем из бакета MinIO
async def get_photo(name: str):
    return await client.presigned_get_object(BUCKET_NAME, name)


# Функция для удаления фотографий, связанных с определенным элементом (Item)
async def delete_photos(itemId: UUID):
    # Получение списка объектов в бакете с префиксом, соответствующим идентификатору элемента
    objects_to_delete = await client.list_objects(BUCKET_NAME, prefix=str(itemId), recursive=True)
    # Перебор списка объектов и удаление каждого объекта
    for obj in objects_to_delete:
        await client.remove_object(BUCKET_NAME, obj.object_name)


# Функция для сохранения фотографии в бакет MinIO
async def save_photo(itemId: UUID, photo: UploadFile):
    # Загрузка файла в бакет с помощью метода put_object
    # Имя файла формируется путем объединения идентификатора элемента и имени файла фотографии
    await client.put_object(BUCKET_NAME, f'{itemId}/{photo.filename}',
                            length=photo.size,
                            data=photo.file,
                            content_type=photo.content_type
                            )
