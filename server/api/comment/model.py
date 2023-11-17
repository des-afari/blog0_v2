from sqlalchemy import Column, String, Integer, ForeignKey, func, TIMESTAMP
from db.base import Base


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(String(255), ForeignKey('users.id'), nullable=False)
    article_id = Column(String(255), ForeignKey('articles.id'), nullable=False)
    comment = Column(String(1000), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=func.now())

    def __repr__(self) -> str:
        return f"<Comment id={self.id} article_id={self.article_id} />"
