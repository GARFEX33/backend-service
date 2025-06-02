import os
from dotenv import load_dotenv

load_dotenv()

SQLMODEL_DATABASE_URL = os.getenv("DATABASE_URL")