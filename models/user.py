import datetime
from models.base import Base
from sqlalchemy import Column, Integer, TIMESTAMP, String, UniqueConstraint


class User(Base):

    __tablename__ = "user"
    __table_args__ = (UniqueConstraint("username", name="unique_username"),)


    id = Column(Integer, primary_key=True)
    create_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    username = Column(String, nullable=False)
    short_description = Column(String, nullable=False)
    long_bio = Column(String)