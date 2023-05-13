from decouple import config
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

engine = create_engine(URL.create(
    drivername='postgresql',
    username=config('USERNAME_DB', cast=str),
    password=config('PASSWORD_DB', cast=str),
    database=config('DATABASE_DB', cast=str),
    host=config('HOST_DB', cast=str),
    port=config('PORT_DB', cast=int),
))

db_session = scoped_session(sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine))

class Base(DeclarativeBase):
    pass

Base.query = db_session.query_property()

def init_db():
    import potatopy.models
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
