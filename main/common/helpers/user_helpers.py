from faker import Faker
from typing import Dict, Any, Optional

fake = Faker()


def safe_email_translation():
    return str.maketrans({",": ".", "-": ".", " ": "_"})


def generate_user(tz: Optional[str] = None) -> Dict[str, Any]:
    """
    Example how we can generate user or company or other system roles
    """
    company = fake.company()
    safe_company = company.translate(safe_email_translation())
    state = fake.state_abbr()
    return {
        "company_name": company,
        "address": fake.street_address(),
        "suite": fake.secondary_address(),
        "city": fake.city(),
        "state": state,
        "zip": fake.zipcode(),
        "phone": fake.phone_number()[4:],
        "fax": fake.phone_number()[4:],
        "email": "auto_test+{name}@test.com".format(name=safe_company),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "password_hash": "password",
        "tz": tz or fake.timezone(),
    }
