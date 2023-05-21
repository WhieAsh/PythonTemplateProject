import datetime
from models.base import Base
from sqlalchemy import Column, Integer, TIMESTAMP, String, UniqueConstraint, ForeignKeyConstraint, Index


class LikedPost(Base):

    __tablename__ = "liked_post"
    __table_args__ = (UniqueConstraint("user_id", "post_id", name="unique_user_id_post_id"),
                      ForeignKeyConstraint(["user_id"], ["user.id"], name="FK_USER_ID"))

    id = Column(Integer, primary_key=True)
    create_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    user_id = Column(Integer)
    post_id = Column(Integer)


Index("user_id_idx", LikedPost.user_id)