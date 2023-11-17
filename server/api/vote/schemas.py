from pydantic import BaseModel


class VoteResponse(BaseModel):
    article_id: str
    user_id: str

    class Config:
        from_attributes = True


class VoteOutcome(BaseModel):
    message: str

    class Config:
        from_attributes = True


