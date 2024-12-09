from passlib.context import CryptContext
passwd_context=CryptContext(
    schemes=["bcrypt"],
)
def generate_passwd_hash(password:str)->str:
    return passwd_context.hash(password)

def verify_passwd(plain_password:str,hashed_password:str)->bool:
    return passwd_context.verify(plain_password,hashed_password)