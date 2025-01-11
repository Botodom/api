from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from functools import wraps
from utils.appwriteClient import AppwriteClient
from appwrite.client import AppwriteException
from os import getenv


security = HTTPBearer()

def require_user_auth(func):
    @wraps(func)
    async def decorated_function(request: Request, *args, **kwargs):
        credentials: HTTPAuthorizationCredentials = await security(request)
        if credentials:

            token = credentials.credentials
            if verify_token(token, route=request.url.path):  
                return await func(request, *args, **kwargs)
        raise HTTPException(status_code=403, detail="Not authenticated")
    
    return decorated_function


def verify_token(token: str, route: str) -> bool:
    try:
        appwrite = AppwriteClient(False, token)
        account = appwrite.account.get()
        if account["emailVerification"] == True:
            return True
        if account["emailVerification"] == False and route == "/v1/eligibility":
            return True
    except AppwriteException:
        return False
    except:
        return HTTPException(status_code=500, detail="Unable to process request.")


def require_admin_auth(func):
    @wraps(func)
    async def decorated_function(request: Request, *args, **kwargs):
        credentials: HTTPAuthorizationCredentials = await security(request)
        if credentials:

            key = credentials.credentials
            if verify_admin(key):  
                return await func(request, *args, **kwargs)
        raise HTTPException(status_code=403, detail="Not authenticated")
    
    return decorated_function


def verify_admin(key: str) -> bool:
    try:
        if key == getenv("SECRET_KEY"):
            return True
        else:
            return False

    except:
        return HTTPException(status_code=500, detail="Unable to process request.")
