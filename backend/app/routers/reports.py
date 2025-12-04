from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import UserInDB
from app.schemas.report import ReportCreate, ReportOut
from app.services.auth import get_current_active_user
from app.db.database import get_database
from app.models.report import WeeklyReport
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=ReportOut)
async def create_weekly_report(
    report: ReportCreate,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    db = get_database()
    report_entry = WeeklyReport(**report.dict(), user_id=str(current_user.id))
    result = await db["reports"].insert_one(report_entry.dict(by_alias=True, exclude_unset=True))
    report_entry.id = str(result.inserted_id)
    return report_entry

@router.get("/", response_model=List[ReportOut])
async def get_user_reports(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    db = get_database()
    reports = []
    async for report_data in db["reports"].find({"user_id": str(current_user.id)}).sort("created_at", -1):
        reports.append(ReportOut(**report_data))
    return reports

@router.get("/{report_id}", response_model=ReportOut)
async def get_report_by_id(
    report_id: str,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    db = get_database()
    report_data = await db["reports"].find_one({"_id": ObjectId(report_id), "user_id": str(current_user.id)})
    if not report_data:
        raise HTTPException(status_code=404, detail="Report not found")
    return ReportOut(**report_data)

@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(
    report_id: str,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    db = get_database()
    result = await db["reports"].delete_one({"_id": ObjectId(report_id), "user_id": str(current_user.id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Report not found")
    return

