# API Endpoints for a thing that we all hate: homework

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



@router.get("/v1/homeworks", response_model=dict)
@require_user_auth
async def get_all_homework(request: Request):
    try:
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1] if " " in auth_header else None

        user = AppwriteClient(False, token)

        docs = user.databases.list_documents(getenv("APPWRITE_DB_ID"), getenv("APPWRITE_HOMEWORK_COLLECTION_ID"))
        
       

        response = {
            "success": True,
            "message": "Homeworks retrieved successfully.",
            "data": [
            {
                "id": doc["$id"],
                "title": doc["title"],
                "description": doc["description"],
                "subject": doc["subject"],
                "deadline": doc["deadline"],
                "notifications": doc["notifications"],
                "completed": doc["completed"],
                "created_at": doc["$createdAt"],
            }
            for doc in docs["documents"]
            ]
        }
        return response
    except:
        raise HTTPException(status_code=500, detail="Unable to process request.")




@router.post("/v1/homework", response_model=dict)
@require_user_auth
async def add_homework(request: Request):
    try:
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1] if " " in auth_header else None

        user = AppwriteClient(False, token)
        user_id = user.account.get()["$id"]
        try:
            data = await request.json()
        except:
            raise BadRequest("The request body is not a valid JSON.", "body_json_invalid")
        try:
            homework = Homework(**data)
        except:
            raise BadRequest("Some required fields are missing", "missing_required_fields")

        perms = [
            permission.read(role.user(user_id)),
            permission.write(role.user(user_id)),
            permission.delete(role.user(user_id)),

            # Admin
            permission.read(role.team("admin")),
            permission.write(role.team("admin")),
            permission.delete(role.team("admin")),
        ]
        doc = user.databases.create_document(database_id=getenv("APPWRITE_DB_ID"), collection_id=getenv("APPWRITE_HOMEWORK_COLLECTION_ID"), document_id=id.unique(), data=homework.model_dump(), permissions=perms)
        
        response = {
            "success": True,
            "message": "Homework added successfully.",
            "data": {
                "id": doc["$id"],
                "title": doc["title"],
                "description": doc["description"],
                "subject": doc["subject"],
                "deadline": doc["deadline"],
                "notifications": doc["notifications"],
                "completed": doc["completed"],
                "created_at": doc["$createdAt"],
            }
        }
        return response
    except JSONDecodeError:
        raise BadRequest("The request body is not a valid JSON.", "body_json_invalid")
    except AppwriteException as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unable to process request.")




@router.get("/v1/homework/{homework_id}", response_model=dict)
@require_user_auth
async def get_homework(request: Request, homework_id: str):
    try:
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1] if " " in auth_header else None

        user = AppwriteClient(False, token)

        doc = user.databases.get_document(getenv("APPWRITE_DB_ID"), getenv("APPWRITE_HOMEWORK_COLLECTION_ID"), homework_id)

        response = {
            "success": True,
            "message": "Homework retrieved successfully.",
            "data": {
                "id": doc["$id"],
                "title": doc["title"],
                "description": doc["description"],
                "subject": doc["subject"],
                "deadline": doc["deadline"],
                "notifications": doc["notifications"],
                "completed": doc["completed"],
                "created_at": doc["$createdAt"],
            }
        }
        return response
    
    except AppwriteException as e:
        if e.type == "document_not_found":
            raise BadRequest("The homework does not exist", "homework_not_found")
        
        raise HTTPException(status_code=500, detail="Unable to process request.")




@router.delete("/v1/homework/{homework_id}", response_model=dict)
@require_user_auth
async def delete_homework(request: Request, homework_id: str):
    try:
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1] if " " in auth_header else None

        user = AppwriteClient(False, token)

        user.databases.delete_document(getenv("APPWRITE_DB_ID"), getenv("APPWRITE_HOMEWORK_COLLECTION_ID"), homework_id)

        return {"success": True, "message": "Homework deleted successfully."}
    except AppwriteException as e:

        if e.type == "document_not_found":
            raise BadRequest("The homework does not exist", "homework_not_found")
        
        raise HTTPException(status_code=500, detail="Unable to process request.")