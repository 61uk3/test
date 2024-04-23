import sqlalchemy
from sqlalchemy import Column, String,Date, ForeignKey, UUID, BOOLEAN
from sqlalchemy.orm import relationship

from database.PostgresDb import Base

class Items(Base):
    __tablename__ = 'lots'
    id = Column(UUID, primary_key=True,index=True)
    name = Column(String)
    active = Column(BOOLEAN)
    description = Column(String)
    date = Column(Date)
    address = Column(String)
    id_Users = Column(UUID,ForeignKey("users.id"))
    id_Categories = Column(UUID,ForeignKey("categories.id"))
    id_Conditions = Column(UUID,ForeignKey("conditions.id"))

    user = relationship('Users', back_populates='items')
    photo = relationship('Photos', back_populates='item')

class Towns(Base):
    __tablename__ = 'towns'
    id = Column(UUID, primary_key=True,index=True)
    town = Column(String)

class Categories(Base):
    __tablename__ = 'categories'
    id = Column(UUID, primary_key=True,index=True)
    category = Column(String)

class Conditions(Base):
    __tablename__ = 'conditions'
    id = Column(UUID, primary_key=True,index=True)
    condition = Column(String)

class Users(Base):
    __tablename__ = 'users'
    id = Column(UUID, primary_key=True,index=True)
    name = Column(String(20))
    login = Column(String(20))
    password = Column(String(64))
    contact = Column(String(30))
    datereg = Column(Date)
    id_town = Column(UUID)
    photo = Column(String)

    items = relationship('Items', back_populates='user')
    #chats = relationship('Chats', back_populates='user')

# class Messages(Base):
#     __tablename__ = 'Сообщения'
#     id_отправителя = Column(UUID,ForeignKey("Пользователи.id_пользователя"))
#     Дата = Column(Date)
#     Сообщение = Column(String)
#     id_чата_Чаты = Column(UUID,ForeignKey("Чаты.id_чата"))



class Chats(Base):
    __tablename__ = 'Чаты'
    id_чата = Column(UUID, primary_key=True,index=True)
    id_пользователя1 = Column(UUID,ForeignKey("Пользователи.id_пользователя"))
    id_пользователя2 = Column(UUID,ForeignKey("Пользователи.id_пользователя"))
    id_лота_Лоты =Column(UUID,ForeignKey("Лоты.id_лота"))

    # user = relationship('Users', back_populates='chats')

class Photos(Base):
    __tablename__ = 'photos'
    id = Column(UUID, primary_key=True,index=True)
    photo = Column(String)
    id_lots = Column(UUID, ForeignKey("lots.id"))

    item = relationship('Items', back_populates='photo')
