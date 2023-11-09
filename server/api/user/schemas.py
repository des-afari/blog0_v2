from pydantic import BaseModel, EmailStr


class JWTResponse(BaseModel):
    id: str
    jti: str
    role: str

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    id: str
    jti: str
    role: str

    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class LogoutSchema(BaseModel):
    access_token: str|None


class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class UserUpdateSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str



class PasswordUpdateSchema(BaseModel):
    current_password: str
    new_password: str


class PasswordUpdateResponse(BaseModel):
    message: str = 'Password updated successfully'