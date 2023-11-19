from pydantic import BaseModel


class CategorySchema(BaseModel):
    parent_id: int = None
    name: str


class CategoryResponse(BaseModel):
    id: int
    parent_id: int | None
    name: str

    class Config:
        from_attributes = True