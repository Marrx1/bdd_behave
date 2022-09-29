import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.environ.get("HOST")
USER_NAME = os.environ.get("USER_NAME")
USER_PASSWORD = os.environ.get("USER_PASSWORD")
SCHEMA = os.environ.get("SCHEMA", "https")
