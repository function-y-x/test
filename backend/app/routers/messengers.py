from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import UserInDB
from app.schemas.messenger import MessengerCreate, MessengerOut
from app.services.auth import get_current_active_user
from app.db.database import get_database
from app.models.messenger import MessengerEntry
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=MessengerOut)
async def create_messenger_entry(
    message: MessengerCreate,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    db = get_database()
    message_entry = MessengerEntry(**message.dict(), user_id=str(current_user.id))
    result = await db["messengers"].insert_one(message_entry.dict(by_alias=True, exclude_unset=True))
    message_entry.id = str(result.inserted_id)
    return message_entry

@router.get("/", response_model=List[MessengerOut])
async def get_user_messages(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    db = get_database()
    messages = []
    async for message_data in db["messengers"].find({"user_id": str(current_user.id)}).sort("created_at", -1):
        messages.append(MessengerOut(**message_data))
    return messages

@router.get("/{message_id}", response_model=MessengerOut)
async def get_message_by_id(
    message_id: str,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    db = get_database()
    message_data = await db["messengers"].find_one({"_id": ObjectId(message_id), "user_id": str(current_user.id)})
    if not message_data:
        raise HTTPException(status_code=404, detail="Message entry not found")
    return MessengerOut(**message_data)

@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: str,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    db = get_database()
    result = await db["messengers"].delete_one({"_id": ObjectId(message_id), "user_id": str(current_user.id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Message entry not found")
    return

