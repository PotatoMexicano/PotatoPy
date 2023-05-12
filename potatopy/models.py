from datetime import datetime
from typing import Optional
from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, DateTime
from werkzeug.security import generate_password_hash

from potatopy.database import Base, db_session

@dataclass
class Usuario(Base):

    __tablename__ = 'usuarios'

    id = Column(Integer, autoincrement=True, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    senha = Column(String(256), nullable=False)
    create_at = Column(DateTime, default=datetime.now, nullable=False)

    def __init__(self, login: str, senha: str):
        self.login = login
        self.senha = generate_password_hash(senha)

    def __repr__(self) -> str:
        return f'User(login={self.login})'

    def get_by_id(pk: int) -> Optional['Usuario']:
        return db_session.query(Usuario).where(Usuario.id == pk).one_or_none()

    def get_by_login(login: str) -> Optional['Usuario']:
        return db_session.query(Usuario).where(Usuario.login == login).one_or_none()

    def register(self) -> Optional['Usuario']:
        try:
            db_session.add(self)
            db_session.commit()
            db_session.refresh(self)

            return self
        except Exception as err:
            print(err)
            return None
