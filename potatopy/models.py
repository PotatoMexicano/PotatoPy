from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import json

from flask import g, jsonify
from sqlalchemy import Column, DateTime, Integer, String
from werkzeug.security import generate_password_hash
from flask_login import UserMixin, current_user

from potatopy.database import Base, db_session
from potatopy import login_manager, app

@dataclass
class Usuario(Base, UserMixin):

    __tablename__ = 'usuarios'

    id = Column(Integer, autoincrement=True, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    senha = Column(String(256), nullable=False)
    role = Column(String(20), nullable=False, default='user')
    create_at = Column(DateTime, default=datetime.now, nullable=False)

    def __init__(self, login: str, senha: str):
        self.login = login
        self.senha = generate_password_hash(senha)

    def __repr__(self) -> str:
        return f'User(login={self.login}, role={self.role})'

    def to_dict(self) -> str:
        return {
            'id': self.id,
            'login': self.login,
            'role': self.role,
            'create_at': self.create_at.timestamp()
        }

    @app.before_request
    def load_logged_in_user():
        g.user = current_user

    @login_manager.user_loader
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

    def update(self, values: dict) -> Optional['Usuario']:

        for index, value in values.items():
            setattr(self, index, value)
        
        db_session.commit()
        db_session.refresh(self)
        
        return self
