# API Endpoints for the elegibility tingy

from fastapi import APIRouter, HTTPException
from appwrite.exception import AppwriteException
from exceptions.exceptions import BadRequest, NotFound
from utils.requires_auth import require_user_auth, require_admin_auth
from utils.appwriteClient import AppwriteClient
from fastapi import Request
from os import getenv
from models.eligibility import EligibilitySend
from appwrite import query as _query
from appwrite import permission as _permission
from appwrite import role as _role
from appwrite import id as _id
from json import JSONDecodeError


router = APIRouter()
permission = _permission.Permission()
role = _role.Role()
id = _id.ID()
admin_appwrite = AppwriteClient(True)


@router.get("/v1/eligibility", response_model=dict, status_code=200)
@require_user_auth
async def get_elegibility(request: Request):
    try:
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1] if " " in auth_header else None

        user = AppwriteClient(False, token)

        docs = user.databases.list_documents(getenv("APPWRITE_DB_ID"), getenv("APPWRITE_ELIGIBILITY_COLLECTION_ID"))
        
       

        if docs["total"] == 0:
            raise NotFound("No eligibility data found for this user.", "not_found")

        doc = docs["documents"][0]
        response = {
            "success": True,
            "message": "Eligibility data retrieved successfully.",
            "data": {
                "submissionID": doc["$id"],
                "userID": doc["userID"],
                "status": doc["status"],
                "reason": doc["reason"]
            }
        }
        return response
    
    except AppwriteException as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unable to process request.")




@router.post("/v1/eligibility", response_model=dict, status_code=201)
@require_user_auth
async def submit_eligibility(request: Request):
    try:
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1] if " " in auth_header else None

        user = AppwriteClient(False, token)
        account = user.account.get()
        user_id = account["$id"]
        if account["emailVerification"] == True:
            raise BadRequest("Your account is already verified.", "already_verified")

        existing_docs = user.databases.list_documents(
            database_id=getenv("APPWRITE_DB_ID"),
            collection_id=getenv("APPWRITE_ELIGIBILITY_COLLECTION_ID"),
            queries=[_query.Query("", "userID", user_id).equal("userID", user_id)]
        )

        if existing_docs["total"] > 0:
            raise BadRequest("Eligibility submission already exists for this user.", "eligibility_exists")

        eligibility_data = {
            "userID": user_id,
            "status": "pending",
            "reason": "We are currently reviewing your eligibility submission. Please expect a response soon."
        }
        try:
            req_data = await request.json()
            accessInput = req_data["accessInput"]
            eligibility_data["accessInput"] = accessInput
            discoverInput = req_data["discoverInput"]
            eligibility_data["discoverInput"] = discoverInput
        except:
            raise BadRequest("Some required fields are missing", "missing_required_fields")
        

        elegibility = EligibilitySend(**eligibility_data)
        perms = [
            permission.read(role.user(user_id)),

            # Admin
            permission.read(role.team("admin")),
            permission.write(role.team("admin")),
            permission.delete(role.team("admin")),
        ]
        doc = user.databases.create_document(database_id=getenv("APPWRITE_DB_ID"), collection_id=getenv("APPWRITE_ELIGIBILITY_COLLECTION_ID"), document_id=id.unique(), data=elegibility.model_dump(), permissions=perms)
        
        admin_appwrite.users.update_labels(user_id, ["pending"])
        response = {
            "success": True,
            "message": "Elegibility data added successfully.",
            "data": {
                "submissionID": doc["$id"],
                "userID": doc["userID"],
                "status": doc["status"],
                "reason": doc["reason"]
            }
        }
        return response
    except JSONDecodeError:
        raise BadRequest("The request body is not a valid JSON.", "body_json_invalid")
    except AppwriteException as e:
        print(e)
        
        raise HTTPException(status_code=500, detail="Unable to process request.")


