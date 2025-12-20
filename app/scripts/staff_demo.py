import asyncio

from app.core.database import mongo_db
from app.services.staff_service import StaffService


async def main():
    await mongo_db.connect()

    staff = await StaffService.create_staff(full_name="yas rohani", employee_code="EMP-002")
    print("Created:", staff.full_name)

    fetched = await StaffService.get_by_employee_code("EMP-001")
    print("Fetched:", fetched.full_name)

    updated = await StaffService.update_staff(
        staff=fetched,
        full_name="yasaman rohani"
    )
    print("Updated:", updated.full_name)

    await mongo_db.close()
    


if __name__ == "__main__":
    asyncio.run(main())