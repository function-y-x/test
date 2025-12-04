from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import UserInDB
from app.schemas.error import ErrorCreate, ErrorUpdate, ErrorOut
from app.services.auth import get_current_active_user
from app.db.database import get_database
from app.models.error import ErrorEntry
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=ErrorOut)
async def create_error_entry(
    error: ErrorCreate,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    db = get_database()
    error_entry = ErrorEntry(**error.dict(), user_id=str(current_user.id))
    result = await db["errors"].insert_one(error_entry.dict(by_alias=True, exclude_unset=True))
    error_entry.id = str(result.inserted_id)
    return error_entry

@router.get("/", response_model=List[ErrorOut])
async def get_user_errors(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    db = get_database()
    errors = []
    async for error_data in db["errors"].find({"user_id": str(current_user.id)}).sort("created_at", -1):
        errors.append(ErrorOut(**error_data))
    return errors

@router.put("/{error_id}", response_model=ErrorOut)
async def update_error(
    error_id: str,
    error_update: ErrorUpdate,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    db = get_database()
    existing_error = await db["errors"].find_one({"_id": ObjectId(error_id), "user_id": str(current_user.id)})
    if not existing_error:
        raise HTTPException(status_code=404, detail="Error entry not found")

    updated_data = error_update.dict(exclude_unset=True)
    if updated_data:
        await db["errors"].update_one(
            {"_id": ObjectId(error_id)},
            {"$set": updated_data}
        )
        updated_error_data = await db["errors"].find_one({"_id": ObjectId(error_id)})
        return ErrorOut(**updated_error_data)
    return ErrorOut(**existing_error)

@router.delete("/{error_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_error(
    error_id: str,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    db = get_database()
    result = await db["errors"].delete_one({"_id": ObjectId(error_id), "user_id": str(current_user.id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Error entry not found")
    return

