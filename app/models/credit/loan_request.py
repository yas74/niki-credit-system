from typing import Optional
from datetime import datetime

from enum import Enum
from beanie import Document
from pydantic import Field

from app.core.time import utc_now


class LoanRequestStatus(str, Enum):
    REQUESTED = "requested"
    APPROVED = "approved"
    REJECTED = "rejected"

class RepaymentMethod(str, Enum):
    SALARY = "salary"
    MANUAL = "manual"   # future

class RepaymentInterval(str, Enum):
    MONTHLY = "monthly"
    BIWEEKLY = "biweekly"
    WEEKLY = "weekly"

class LoanRequest(Document):
    business_id: str
    staff_id: str

    amount: int
    installments_count: int
    interval: RepaymentInterval = RepaymentInterval.MONTHLY

    requested_repayment_method: RepaymentMethod = RepaymentMethod.SALARY
    status: LoanRequestStatus = LoanRequestStatus.REQUESTED

    note: Optional[str] = None

    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None

    created_at: datetime = Field(default_factory=utc_now)

    class Settings:
        name = "loan_requests"