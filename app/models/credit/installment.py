from datetime import datetime
from enum import Enum
from typing import Annotated, Optional

from beanie import Document, Indexed

class InstallmentStatus(str, Enum):
    PENDING = "pending"
    LATE = "late"
    PAYED = "payed"

class Installment(Document):
    business_id: str
    loan_id: Annotated[str, Indexed()]
    staff_id: str

    sequence_number: int    
    amount: int
    due_date: datetime

    status: InstallmentStatus = InstallmentStatus.PENDING

    paid_at: Optional[datetime] = None
    notified_at: Optional[datetime] = None

    class Settings:
        name = "installments"

