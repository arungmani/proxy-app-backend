import jwt
from jwt import PyJWTError
from fastapi import APIRouter, Depends, HTTPException, Request

SECRET_KEY = "secret_123"


async def verify_jwt(request: Request):
    token = request.headers.get("Authorization")
    if token is None or not token.startswith("Bearer"):
        raise HTTPException(status_code=403, detail="Authorization header missing")
    token = token[len("Bearer "):]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    
        return payload.get("data")
    except PyJWTError:
        raise HTTPException(status_code=403, detail="Invalid or expired token")
