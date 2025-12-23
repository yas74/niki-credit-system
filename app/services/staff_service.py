from typing import Optional, Tuple, List
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
    async def list_staff(
        *,
        limit: int = 10,
        cursor: Optional[PydanticObjectId] = None
    ) -> Tuple[List[Staff], bool]:
        """
        Returns a list of staff ordered by _id ASC using cursor-based pagination.

        :param limit: max number of items to return
        :param cursor: last seen staff _id
        :return: (items, has_more)
        """

        # Enforce upper bound defensively (service-level safety)
        limit = min(limit, 50)

        query = Staff.find()

        if cursor is not None:
            query = query.find(Staff.id > cursor)

        items = (
            await query
            .sort(Staff.id)
            .limit(limit + 1)
            .to_list()
        )

        has_more = len(items) > limit

        if has_more:
            items = items[:limit]

        return items, has_more

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

    @staticmethod
    async def deactivate_staff(staff_id: PydanticObjectId) -> Staff:
        """
        Deactivate (soft-delete) a staff member.

        Rules:
        - Staff must exist
        - Staff must be active
        - Deactivation is NOT idempotent (second call is an error)
        """

        staff = await Staff.get(staff_id)

        if staff is None:
            raise ValueError("STAFF_NOT_FOUND")
        
        if not staff.is_active:
            raise ValueError("STAFF_ALREADY_DEACTIVATED")
        
        staff.is_active = False
        await staff.save()

        return staff