
from fastapi import APIRouter, HTTPException
from appwrite.exception import AppwriteException
from exceptions.exceptions import BadRequest
from utils.requires_auth import require_user_auth
from utils.appwriteClient import AppwriteClient
from fastapi import Request
from os import getenv
from models.homework import Homework
from appwrite import id as _id
from appwrite import permission as _permission
from appwrite import role as _role
from json import JSONDecodeError


router = APIRouter()
id = _id.ID()
permission = _permission.Permission()
role = _role.Role()



@router.get("/v1/verify", response_model=dict)
async def verify_account(request: Request):
    try:
        user_id = request.query_params.get("userId")
        secret = request.query_params.get("secret")
        
        if not user_id or not secret:
            return "Invalid Request!"
        
        
        client = AppwriteClient(False)
        try:
            verification = client.account.update_verification(user_id, secret)
        except AppwriteException as e:
            print(e.type)
            return {"message": f"Account already verified or invalid token"}
        return {"message": f"Account verified successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unable to process request.")


