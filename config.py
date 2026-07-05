from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACESS_TOKEN_EXPIREM = os.getenv("ACESS_TOKEN_EXPIREM")

bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

OAuth2_schema = OAuth2PasswordBearer(
    tokenUrl="/login"
)
