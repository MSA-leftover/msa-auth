from ..settings import get_settings, ProjectSettings
import datetime
from jose import jwt
from ..connections import redis_client

settings: ProjectSettings = get_settings()


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt.secret, algorithm=settings.jwt.algorithm
    )
    # Store the token and its expiration time in Redis
    token_key = f"token:{encoded_jwt}"
    expiration_time = datetime.datetime.now() + datetime.timedelta(
        seconds=settings.jwt.expiration
    )
    redis_client.set(token_key, encoded_jwt)
    redis_client.expireat(token_key, int(expiration_time.timestamp()))
    return encoded_jwt
