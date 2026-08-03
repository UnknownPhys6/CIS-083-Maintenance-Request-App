from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

password = "7upisGood"

hashed = pwd_context.hash(password)

print(hashed)