import os
from datetime import timedelta
from uuid import UUID

from aiohttp import FormData
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
    return await client.presigned_get_object(BUCKET_NAME,
                                             name,
                                             expires=timedelta(seconds=604800),
                                             # Время жизни URL в секундах (например, 7 дней)
                                             response_headers={"response-content-disposition": "inline"})


# Функция для удаления фотографий, связанных с определенным элементом (Item)
async def delete_photos(itemId: UUID):
    # Получение списка объектов в бакете с префиксом, соответствующим идентификатору элемента
    objects_to_delete = await client.list_objects(BUCKET_NAME, prefix=str(itemId), recursive=True)
    # Перебор списка объектов и удаление каждого объекта
    for obj in objects_to_delete:
        await client.remove_object(BUCKET_NAME, obj.object_name)


# Функция для сохранения фотографии в бакет MinIO
async def save_photo(itemId: UUID, photo: UploadFile):
    # Формирование объекта FormData для отправки файла
    form_data = FormData()
    form_data.add_field('file',
                        photo.file,
                        filename=photo.filename,
                        content_type= 'image/jpg')  # Устанавливаем правильный Content-Type

    # Загрузка файла в бакет с помощью метода put_object
    # Имя файла формируется путем объединения идентификатора элемента и имени файла фотографии
    object_key = f'{itemId}/{photo.filename}'
    await client.put_object(BUCKET_NAME, object_key, data=form_data)