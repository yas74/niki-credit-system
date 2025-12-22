from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class StaffCreateRequest(BaseModel):
    full_name: str = Field(..., min_length=1)
    employee_code: str = Field(..., min_length=1)

class StaffResponse(BaseModel):
    id: str
    full_name: str
    employee_code: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

class StaffListResponse(BaseModel):
    items: List[StaffResponse]
    next_cursor: Optional[str]
    has_more: bool