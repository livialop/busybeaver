# pip install mysqlclient
# pip install sqlalchemy
# pip install sqlalchemy_utils
from sqlalchemy import create_engine, String, DateTime, Integer, ForeignKey, Text, Float
from sqlalchemy.orm import Session, Mapped, mapped_column, DeclarativeBase, sessionmaker, relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import create_database, database_exists
from typing import List, Optional
from datetime import datetime

DATABASE = 'mysql+mysqldb://root@localhost/busybeaver'
engine = create_engine(DATABASE)

class Base(DeclarativeBase):
    pass

from flask_login import UserMixin

class User(Base, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(120))
    password: Mapped[str] = mapped_column(String(300))

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    preco: Mapped[float] = mapped_column(Float, nullable=False)
    descricao: Mapped[str] = mapped_column(String(200))  

    def __repr__(self):
        return f"Product(id={self.id!r}, nome={self.nome!r}, preco={self.preco!r})"

def create_db(engine):
    # Creating database
    try:
        if not database_exists(engine.url):
            create_database(engine.url)
            print(database_exists(engine.url))
    except Exception as e:
        print(f"Erro para criar o banco: {e}")
        return

    # Creating tables
    try: 
        Base.metadata.create_all(engine)
        print("Tabelas criadas com sucesso.")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")

def get_session():
    Session = sessionmaker(bind=engine)
    return Session()

if __name__ == "__main__":
    create_db(engine=engine)