import re


def nomalize_iran_phone(phone: str) -> str:
    """
    Accepts:
      - 09123456789
      - +989123456789

    Returns:
      - +989123456789

    Raises:
      ValueError("INVALID_PHONE_NUMBER")
    """
    phone = phone.strip()

    if re.fullmatch(r"0\d{10}", phone):
        return "+98" + phone[1:]
    
    if re.fullmatch(r"\+98\d{10}", phone):
        return phone
    
    raise ValueError("INVALID_PHONE_NUMBER")
