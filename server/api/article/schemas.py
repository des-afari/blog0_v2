from pydantic import BaseModel
from typing import List
from datetime import datetime
from api.category.schemas import CategoryResponse
from api.comment.schemas import CommentResponse
from api.vote.schemas import VoteResponse


class ArticleSchema(BaseModel):
    img_url: str
    title: str
    description: str
    content: str
    categories: List[str]


class ArticleUpdateSchema(BaseModel):
    img_url: str = None
    title: str = None
    description: str = None
    content: str = None
    

class ArticleResponse(BaseModel):
    id: str
    img_url: str
    title: str
    description: str
    content: str
    created_at: datetime
    updated_at: datetime | None
    categories: List[CategoryResponse]
    comments: List[CommentResponse]
    votes: List[VoteResponse]

    class Config:
        from_attributes = True
