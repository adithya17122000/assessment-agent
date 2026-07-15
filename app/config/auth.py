from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config.settings import SERVICE_ACCESS_TOKEN

bearer_scheme = HTTPBearer()


def verify_service_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials.credentials != SERVICE_ACCESS_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid access token")