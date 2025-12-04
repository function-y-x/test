from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field

class ErrorEntry(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: str
    description: str
    image_url: Optional[str] = None
    ai_analysis: Optional[Dict[str, Any]] = None # {type: "概念不清", reason: "..."}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

