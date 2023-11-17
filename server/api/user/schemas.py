from pydantic import BaseModel, EmailStr


class JWTResponse(BaseModel):
    id: str
    jti: str
    role: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class RefreshResponse(BaseModel):
    id: str
    access_token: str
    role: str

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    id: str
    access_token: str
    role: str
    user: UserResponse

    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class LogoutSchema(BaseModel):
    access_token: str|None


class UserUpdateSchema(BaseModel):
    email: EmailStr = None
    first_name: str = None
    last_name: str = None



class PasswordUpdateSchema(BaseModel):
    current_password: str
    new_password: str


class PasswordUpdateResponse(BaseModel):
    message: str = 'Password updated successfully'