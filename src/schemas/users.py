from sqlalchemy import Column, Integer, String, DateTime
from ..connections.database import Base, engine


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(16))
    password = Column(String(255))
    created_at = Column(DateTime)


Base.metadata.create_all(engine)
