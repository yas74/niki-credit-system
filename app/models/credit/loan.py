from datetime import datetime
from typing import Optional
from enum import Enum

from beanie import Document
from pydantic import Field

from app.core.time import utc_now


class GuaranteeType(str, Enum):
    SAFTEH ="safteh"

class LoanStatus(str, Enum):
    PENDING_GUARANTEE = "pending_guarantee"
    ACTIVE = "active"
    COMPLETED = "completed"
    DEFAULTED = "defaulted"

class RepaymentMethod(str, Enum):
    SALARY = "salary"
    MANUAL = "manual"   # future

class RepaymentInterval(str, Enum):
    MONTHLY = "monthly"
    BIWEEKLY = "biweekly"
    WEEKLY = "weekly"

class Loan(Document):
    business_id: str
    staff_id: str

    principal_amount: int
    installments_count: int
    installment_amount: int
    interval: RepaymentInterval = RepaymentInterval.MONTHLY

    repayment_method: RepaymentMethod = RepaymentMethod.SALARY
    status: LoanStatus 

    guarantee_required: bool = False 
    guarantee_delivered: bool = False
    guarantee_type: Optional[GuaranteeType] = None
    guarantee_reference: Optional[str] = None


    started_at: datetime 
    updated_at: datetime = Field(default_factory=utc_now)
    created_from_request_id: str

    class Settings:
        name = "loans"
