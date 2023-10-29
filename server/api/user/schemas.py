from pydantic import BaseModel

class JWTResponse(BaseModel):
    id: str
    jti: str
    role: str

    class Config:
        from_attributes = True