from jwt import encode, decode
from datetime import datetime, timedelta
from conf import SECRET_KEY

def create_token(data: dict) -> str:
    exp_time = datetime.utcnow() + timedelta(minutes=60)
    data.update({'exp': exp_time})
    token: str = encode(payload=data, key=SECRET_KEY, algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    data: dict = decode(token, key=SECRET_KEY, algorithms=['HS256'])
    return data