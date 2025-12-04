from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

class UserInDB(BaseModel):
    id: Optional[str] = Field(alias="_id")
    username: str
    email: str
    hashed_password: str
    exam_date: Optional[datetime] = None
    selected_subjects: Optional[List[str]] = []
    ai_companion_style: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

