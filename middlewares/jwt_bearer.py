from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from datetime import datetime
from utils.jwt_manager import validate_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if not data:
            raise HTTPException(status_code=403, detail="Invalid")

        exp = datetime.fromtimestamp(data.get('exp'))
        now = datetime.now()
        if now > exp:
            raise HTTPException(status_code=401, detail="Token expired")
        #return auth.credentials