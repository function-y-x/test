from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.user import UserInDB
from app.schemas.user import UserUpdate, UserOut
from app.services.auth import get_current_active_user
from app.db.database import get_database
from bson import ObjectId

router = APIRouter()

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: Annotated[UserInDB, Depends(get_current_active_user)]):
    return current_user

@router.put("/me", response_model=UserOut)
async def update_users_me(
    user_update: UserUpdate,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    db = get_database()
    updated_data = user_update.dict(exclude_unset=True)
    if updated_data:
        # Convert ObjectId to string for comparison if needed, but Pydantic handles it
        await db["users"].update_one(
            {"_id": ObjectId(current_user.id)},
            {"$set": updated_data}
        )
        updated_user_data = await db["users"].find_one({"_id": ObjectId(current_user.id)})
        if updated_user_data:
            return UserOut(**updated_user_data)
        raise HTTPException(status_code=404, detail="User not found after update")
    return current_user

