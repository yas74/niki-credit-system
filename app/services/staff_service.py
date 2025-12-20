from typing import Optional
from datetime import datetime, timezone

from beanie import PydanticObjectId

from app.models.staff import Staff


UTC_NOW = lambda: datetime.now(timezone.utc)

class StaffService:
    @staticmethod
    async def create_staff(
        *,
        full_name: str,
        employee_code: str

    ) -> Staff:
        staff = Staff(
            full_name=full_name,
            employee_code=employee_code
        )
        await staff.insert()
        return staff
    
    @staticmethod
    async def get_by_employee_code(employee_code: str) -> Optional[Staff]:
        return await Staff.find_one(Staff.employee_code == employee_code)
    
    @staticmethod
    async def get_by_id(staff_id: PydanticObjectId) -> Optional[Staff]:
        return await Staff.get(staff_id)
    
    @staticmethod
    async def update_staff(
        *,
        staff: Staff,
        full_name: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Staff:
        if full_name is not None:
            staff.full_name = full_name

        if is_active is not None:
            staff.is_active = is_active
        
        staff.updated_at = UTC_NOW()
        await staff.save()
        
        return staff
