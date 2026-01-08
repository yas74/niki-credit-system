from enum import Enum
from typing import Optional
from datetime import datetime, date

from pydantic import BaseModel, Field



class LoanRequestCreate(BaseModel):
    amount: int = Field(..., gt=0)
    installments_count: int = Field(..., gt=0)
    interval: RepaymentInterval
    note: Optional[str] = None

class LoanRequestResponse(BaseModel):
    id: str
    staff_id: str
    amount: int
    installments_counts: int
    interval: RepaymentInterval
    status: LoanRequestStatus
    note: Optional[str] = None
    created_at: datetime
    reviewed_at: Optional[datetime] = None

class LoanResponse(BaseModel):
    id: str
    staff_id: str
    
    principal_amount: int
    installments_count: int
    installment_amount: int
    interval: RepaymentInterval
    repayment_method: RepaymentMethod

    status: LoanStatus

    guarantee_required: bool
    guarantee_delivered: bool
    guarantee_type: Optional[GuaranteeType]
    guarantee_reference: Optional[str]

    started_at: datetime

class InstallmentResponse(BaseModel):
    id: str
    loan_id: str
    sequence_number: int
    amount: int
    due_date: date
    status: InstallmentStatus
    paid_at: Optional[datetime]
    notified_at: Optional[datetime]

class CreditPoolResponse(BaseModel):
    balance: int
    updated_at: datetime

class CreditTransactionResponse(BaseModel):
    id: str
    staff_id: str
    loan_id: Optional[str]
    installment_id: Optional[str]
    amount: int
    type: CreditTransactionType
    created_at: datetime

class CriterionResponse(BaseModel):
    id: str
    name: str
    weight: int
    min_required_score: int
    active: bool

class StaffCriterionScoreCreate(BaseModel):
    criterion_id: str
    score: int
    note: Optional[str] = None

class StaffCriterionScoreResponse(BaseModel):
    id: str
    staff_id: str
    criterion_id: str
    score: int
    reviewed_at: datetime
    reviewed_by: str
    note: Optional[str]

class StaffScoreSummary(BaseModel):
    average_score: float
    total_score: float
    level: int

