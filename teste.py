from passlib.context import CryptContext

bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

print(bcrypt_context.hash("123456"))