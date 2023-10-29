from sqlalchemy import Column, String
from db.base import Base


class JsonTokenId(Base):
    __tablename__ = 'json_token_ids'

    id = Column(String(255), primary_key=True, nullable=False)

    def __repr__(self) -> str:
        return f"<JSsonTokenId id={self.id} />"