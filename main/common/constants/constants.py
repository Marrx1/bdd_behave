FIELD_MAY_NOT_BE_NULL = "This field may not be null."
BOOLEAN_FIELD_ERROR = "Must be a valid boolean."
CODE_IS_REQUIRED = "Code is required"
IS_NOT_A_VALID_CHOICE = '"{}" is not a valid choice.'

DATE_PATTERN = "%Y-%m-%d"
PRESCRIPTION_DATE_PATTERN = "%m/%d/%Y"
DATE_TIME_PATTERN = "%Y-%m-%dT%H:%M:%SZ"
PRESCRIPTION_DATETIME_PATTERN = "%m/%d/%Y %H:%M:%S"
BULLET_UI_DATE_PATTERN = "%m/%d/%Y %H:%M:%S %z"  # '05/31/2022 04:49:34 -0700'

CONTEXT_MAPPING = {
    "patient": "patient.id",
    "practice": "practice_id",
    "prescribing_physician": "physician.id",
}