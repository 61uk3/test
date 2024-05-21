from uuid import UUID
class Photo:
    id: UUID
    photo: str

    def __init__(self,
     id: UUID,
     photo: str):
        self.id = id
        self.photo = photo
