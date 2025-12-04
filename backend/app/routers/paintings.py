from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import UserInDB
from app.schemas.painting import PaintingCreate, PaintingOut
from app.services.auth import get_current_active_user
from app.db.database import get_database
from app.models.painting import PaintingEntry
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=PaintingOut)
async def create_painting_entry(
    painting: PaintingCreate,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    db = get_database()
    painting_entry = PaintingEntry(**painting.dict(), user_id=str(current_user.id))
    result = await db["paintings"].insert_one(painting_entry.dict(by_alias=True, exclude_unset=True))
    painting_entry.id = str(result.inserted_id)
    return painting_entry

@router.get("/", response_model=List[PaintingOut])
async def get_user_paintings(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    db = get_database()
    paintings = []
    async for painting_data in db["paintings"].find({"user_id": str(current_user.id)}).sort("created_at", -1):
        paintings.append(PaintingOut(**painting_data))
    return paintings

@router.get("/{painting_id}", response_model=PaintingOut)
async def get_painting_by_id(
    painting_id: str,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    db = get_database()
    painting_data = await db["paintings"].find_one({"_id": ObjectId(painting_id), "user_id": str(current_user.id)})
    if not painting_data:
        raise HTTPException(status_code=404, detail="Painting entry not found")
    return PaintingOut(**painting_data)

@router.delete("/{painting_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_painting(
    painting_id: str,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    db = get_database()
    result = await db["paintings"].delete_one({"_id": ObjectId(painting_id), "user_id": str(current_user.id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Painting entry not found")
    return

