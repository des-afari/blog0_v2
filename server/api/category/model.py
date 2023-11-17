from sqlalchemy import Column, String, Integer, func, TIMESTAMP
from db.base import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), index=True, unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<Category id={self.id} name={self.name} />"