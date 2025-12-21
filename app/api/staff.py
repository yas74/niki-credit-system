from fastapi import APIRouter, HTTPException, status
from pymongo.errors import DuplicateKeyError

from app.schemas.staff import StaffCreateRequest, StaffResponse
from app.services.staff_service import StaffService


router = APIRouter(prefix="/staff", tags=["staff"])


@router.post(
    "",
    response_model=StaffResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_staff(payload: StaffCreateRequest):
    try:
        staff = await StaffService.create_staff(
            full_name=payload.full_name,
            employee_code=payload.employee_code
        )
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee code already exists"
        )
    
    return StaffResponse(
        id=str(staff.id),
        full_name=staff.full_name,
        employee_code=staff.employee_code,
        is_active=staff.is_active,
        created_at=staff.created_at,
        updated_at=staff.updated_at
    )