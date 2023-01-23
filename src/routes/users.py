from fastapi import APIRouter, HTTPException, Depends
from ..services.user_service import authenticate_user, validate_token, create_user
from ..services.jwt_service import create_access_token
from ..connections.redis import redis_client


router = APIRouter()


@router.post("/signup")
async def sign_up(username: str, password: str):
    await create_user(username, password)
    return {"message": "User registered successfully"}


@router.post("/token")
async def login_for_access_token(username: str, password: str):
    user = await authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token({"sub": user})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(token: str = Depends(validate_token)):
    # Remove the token from Redis
    token_key = f"token:{token}"
    print(token_key)
    redis_client.delete(token_key)
