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
    

ACCESS_PRIVATE_KEY = get_private_key('keys/access/privatekey.pem')
ACCESS_PUBLIC_KEY = get_public_key('keys/access/publickey.pem')
REFRESH_PRIVATE_KEY = get_private_key('keys/refresh/privatekey.pem')
REFRESH_PUBLIC_KEY = get_public_key('keys/refresh/publickey.pem')


def create_token(data: dict, expiry: int, private_key):
    to_encode = data.copy()
    to_encode.update({
        'jti': token_hex(),
        'exp': datetime.utcnow() + timedelta(minutes=expiry)
    })

    return jwt.encode(to_encode, key=private_key, algorithm='RS256')


def verify_token(token: str, public_key, credential_exception):
    try:
        payload = jwt.decode(token, public_key, algorithms=['RS256'])
        id: str = payload.get('id')
        jti: str = payload.get('jti')
        role: str = payload.get('role')

        response = JWTResponse(id=id, jti=jti, role=role)

    except JWTError:
        raise credential_exception
    
    return response


async def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        401, detail='Could not validate credentials', headers={"WWW_Authenticate": "Bearer"}
    )

    payload = verify_token(token, ACCESS_PUBLIC_KEY, credential_exception)

    if db.query(JsonTokenId).filter(JsonTokenId.id == payload.jti).first():
        raise credential_exception
    
    return payload