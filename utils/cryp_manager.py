from bcrypt import gensalt, hashpw

def generate_encrypt(password: str):
    salt = gensalt()
    password_encode = password.encode("utf-8")
    hashed_password = hashpw(password_encode, salt)
    return hashed_password