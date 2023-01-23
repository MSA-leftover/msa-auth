from fastapi import Depends, HTTPException
from ..connections.database import get_db
from ..schemas.users import User
import bcrypt
from jose import jwt
from ..settings import get_settings
from fastapi.security import OAuth2PasswordBearer
import datetime

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
settings = get_settings()


async def authenticate_user(username: str, password: str):
    # check user credentials with database
    db = next(get_db())
    user = db.query(User).filter(User.username == username).first()

    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return username


async def validate_token(
    token: str = Depends(oauth2_scheme),
):
    try:
        payload = jwt.decode(
            token, settings.jwt.secret, algorithms=settings.jwt.algorithm
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    db = next(get_db())
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid token")
    return token


async def create_user(username, password):
    db = next(get_db())
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    new_user = User(
        username=username, password=hashed_password, created_at=datetime.datetime.now()
    )
    db.add(new_user)
    db.commit()
