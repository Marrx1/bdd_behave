
from typing import Dict, Any, Optional

from faker import Faker

fake = Faker()


def luhn_checksum(n: int) -> int:
    """
    Returns the Luhn checksum for ``n`` (``n`` should not
    include the Luhn checksum). The returned value will be in the range
    0 <= value <= 9.

    See https://npiprofile.com/validation.
    """
    import math

    def round_up_to_next_multiple_of_10(x):
        return int(math.ceil(x / 10.0)) * 10

    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer")

    a = [int(x) for x in list(str(n))]  # Split n into list of component digits
    # Double every other digit starting from the last one
    for i in range(len(a) - 1, -1, -2):
        val = a[i] * 2
        if val > 9:
            val -= 9  # Same as adding 2 digits of a number 10 <= val < 20
        a[i] = val
    total = sum(a) + 24
    return round_up_to_next_multiple_of_10(total) - total


def is_valid_luhn_checksum(n: int) -> bool:
    return luhn_checksum(n // 10) == n % 10


def safe_email_translation():
    return str.maketrans({",": ".", "-": ".", " ": "_"})


def append_luhn_checksum(n: int) -> str:
    """Appends the Luhn checksum of n to n"""
    return f"{n}{luhn_checksum(n)}"


def generate_npi() -> int:
    return append_luhn_checksum(fake.random.randint(100000000, 299999999))


def generate_physician(tz: Optional[str] = None) -> Dict[str, Any]:
    """
    Note: NPIs may only begin with a 1 or a 2, so the random
    range for the 9-digit part of the NPI (without checksum) must be
    100000000 - 299999999.
    """
    company = fake.company()
    safe_company = company.translate(safe_email_translation())
    state = fake.state_abbr()
    return {
        "practice_name": company,
        "address": fake.street_address(),
        "suite": fake.secondary_address(),
        "city": fake.city(),
        "state": state,
        "zip": fake.zipcode(),
        "phone": fake.phone_number()[4:],
        "fax": fake.phone_number()[4:],
        "email": "main+{name}@elationhealth.com".format(name=safe_company),
        "first_name": fake.first_name(),
        "middle_name": "J",
        "last_name": fake.last_name(),
        "credentials": "MD",
        "password_hash": "password",
        "npi": generate_npi(),
        "dea": str(fake.random.randint(100000000, 999999999)),
        "license": str(fake.random.randint(100000000, 999999999)),
        "license_state": state,
        "challenge_questions": None,
        "from_npi_db": False,
        "labs": [],
        "user_signature": True,
        "physician_invitation_id": None,
        "activating": True,
        "tz": tz or fake.timezone(),
    }
