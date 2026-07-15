from fastapi import Header, HTTPException
from app.config.settings import SERVICE_ACCESS_TOKEN


def verify_service_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or malformed Authorization header")

    token = authorization.removeprefix("Bearer ").strip()

    if token != SERVICE_ACCESS_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid access token")