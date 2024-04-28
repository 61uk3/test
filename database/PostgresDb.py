from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# Получение URL базы данных из переменной окружения
URL_DATABASE = os.getenv('DB_URL')
# Создание движка SQLAlchemy
engine = create_engine(URL_DATABASE, pool_pre_ping=True)
# Создание сессии для взаимодействия с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Определение базовой модели
Base = declarative_base()


def get_connection():
    con = SessionLocal()
    try:
        yield con
    finally:
        con.close()
