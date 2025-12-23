from typing import Optional

from fastapi import APIRouter, HTTPException, status, Query
from pymongo.errors import DuplicateKeyError
from beanie import PydanticObjectId

from app.schemas.staff import StaffCreateRequest, StaffResponse, StaffListResponse
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

@router.get(
    "/list",
    response_model=StaffListResponse
)
async def list_staff(
    limit: int = Query(10, ge=1, le=50),
    cursor: Optional[PydanticObjectId] = Query(None)
):
    items, has_more = await StaffService.list_staff(
        limit=limit,
        cursor=cursor
    )

    next_cursor = None
    if has_more and items:
        next_cursor = str(items[-1].id)

    return StaffListResponse(
        items=[
            StaffResponse(
                id=str(staff.id),
                full_name=staff.full_name,
                employee_code=staff.employee_code,
                is_active=staff.is_active,
                created_at=staff.created_at,
                updated_at=staff.updated_at
            ) for staff in items
        ],
        has_more=has_more,
        next_cursor=next_cursor
    )

@router.get(
    "/{staff_id}",
    response_model=StaffResponse
)
async def get_staff_by_id(staff_id: PydanticObjectId):
    staff = await StaffService.get_by_id(staff_id)

    if staff is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff not found"
        )
    
    return StaffResponse(
        id=str(staff.id),
        full_name=staff.full_name,
        employee_code=staff.employee_code,
        is_active=staff.is_active,
        created_at=staff.created_at,
        updated_at=staff.updated_at
    )

@router.get(
    "",
    response_model=StaffResponse
)
async def get_staff_by_employee_code(employee_code: str):
    staff = await StaffService.get_by_employee_code(employee_code)

    if staff is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff not found"
        )
    
    return StaffResponse(
        id=str(staff.id),
        full_name=staff.full_name,
        employee_code=staff.employee_code,
        is_active=staff.is_active,
        created_at=staff.created_at,
        updated_at=staff.updated_at
    )

@router.patch(
    "/{staff_id}/deactivate",
    response_model=StaffResponse
)
async def deactivate_staff(staff_id: PydanticObjectId):
    try:
        staff = await StaffService.deactivate_staff(staff_id)
    except ValueError as exc:
        if str(exc) == "STAFF_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff not found"
            )
        if str(exc) == "STAFF_ALREADY_DEACTIVATED":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Staff is already deactivated",
            )
        raise

    return StaffResponse(
        id=str(staff.id),
        full_name=staff.full_name,
        employee_code=staff.employee_code,
        is_active=staff.is_active,
        created_at=staff.created_at,
        updated_at=staff.updated_at,
    )
