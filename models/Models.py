from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import relationship

from database.PostgresDb import Base

class Items(Base):
    __tablename__ = 'Лоты'

