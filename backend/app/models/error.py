from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field, ConfigDict

class ErrorEntry(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
    
    id: Optional[str] = Field(alias="_id")
    user_id: str
    description: str
    image_url: Optional[str] = None
    ai_analysis: Optional[Dict[str, Any]] = None # {type: "概念不清", reason: "..."}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

