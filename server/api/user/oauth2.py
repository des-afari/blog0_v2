from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from utils.session import get_db
from fastapi.security import OAuth2PasswordBearer
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from secrets import token_hex
from datetime import datetime, timedelta
from api.user.schemas import JWTResponse
from api.jti.model import JsonTokenId


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# PATHS
ADMIN_ACCESS_PRIVATE_KEY_PATH = 'keys/admin/access/privatekey.pem'
ADMIN_ACCESS_PUBLIC_KEY_PATH = 'keys/admin/access/publickey.pem'
ADMIN_REFRESH_PRIVATE_KEY_PATH = 'keys/admin/refresh/privatekey.pem'
ADMIN_REFRESH_PUBLIC_KEY_PATH = 'keys/admin/refresh/publickey.pem'
USER_ACCESS_PRIVATE_KEY_PATH = 'keys/user/access/privatekey.pem'
USER_ACCESS_PUBLIC_KEY_PATH = 'keys/user/access/publickey.pem'
USER_REFRESH_PRIVATE_KEY_PATH = 'keys/user/refresh/privatekey.pem'
USER_REFRESH_PUBLIC_KEY_PATH = 'keys/user/refresh/publickey.pem'

def get_private_key(path):
    try:
        with open(path, 'rb') as file:
            return serialization.load_pem_private_key(
                file.read(),
                password=None,
                backend=default_backend()
            )
    except FileNotFoundError:
      raise HTTPException(404, 'Key not found')


def get_public_key(path):
    try:
        with open(path, 'rb') as file:
            return serialization.load_pem_public_key(
                file.read(),
                backend=default_backend()
            )
    except FileNotFoundError:
        raise HTTPException(404, 'Key not found')


def create_token(data: dict, expiry: int, key: str):
    to_encode = data.copy()
    to_encode.update({
        'jti': token_hex(),
        'exp': datetime.utcnow() + timedelta(minutes=expiry)
    })

    return jwt.encode(to_encode, key, algorithm='RS256')


def verify_token(token: str, key: str, credential_exception):
    try:
        payload = jwt.decode(token, key, algorithms=['RS256'])
        id: str = payload.get('id')
        jti: str = payload.get('jti')
        role: str = payload.get('role')

        response = JWTResponse(id=id, jti=jti, role=role)

    except JWTError:
        raise credential_exception
    
    return response


user_public_key = get_public_key(USER_ACCESS_PUBLIC_KEY_PATH)
admin_public_key = get_public_key(ADMIN_ACCESS_PUBLIC_KEY_PATH)


async def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        401, detail='Could not validate credentials', headers={"WWW_Authenticate": "Bearer"}
    )

    payload = verify_token(token, user_public_key, credential_exception)

    if db.query(JsonTokenId).filter(JsonTokenId.id == payload.jti).first():
        raise credential_exception
    
    return payload


async def get_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        401, detail='Could not validate credentials', headers={"WWW_Authenticate": "Bearer"}
    )

    payload = verify_token(token, admin_public_key, credential_exception)

    if db.query(JsonTokenId).filter(JsonTokenId.id == payload.jti).first():
        raise credential_exception
    
    return payload