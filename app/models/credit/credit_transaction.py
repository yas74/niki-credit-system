from datetime import datetime
from typing import Optional, Annotated
from enum import Enum

from pydantic import Field
from beanie import Document, Indexed

from app.core.time import utc_now


class CreditTransactionType(str, Enum):
    LOAN = "loan"
    REPAYMENT = "repayment"
    ADJUSTMENT = "adjustment"

class CreditTransaction(Document):
    business_id: str

    staff_id: Optional[str] = None
    loan_id: Optional[str] = None
    installment_id: Annotated[Optional[str], Indexed()] = None

    amount: int
    type: CreditTransactionType = CreditTransactionType.

    transaction_reference: Optional[str] = None

    created_by: str
    created_at: datetime = Field(default_factory=utc_now)

    class Settings:
        name = "credit_transactions"
