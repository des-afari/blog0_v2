from pydantic import BaseModel
from datetime import datetime


class CommentSchema(BaseModel):
    comment: str


class CommentUserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class CommentResponse(BaseModel):
    id: int
    comment: str
    created_at: datetime
    updated_at: datetime | None
    user: CommentUserResponse

    class Config:
        from_attributes = True
