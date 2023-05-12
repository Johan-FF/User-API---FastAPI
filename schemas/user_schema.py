from pydantic import BaseModel, Field
from typing import Optional

class UserSchema(BaseModel):
    id: Optional[int] = None
    name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)
    nickname: str = Field(max_length=20)
    email: str = Field(max_length=30)
    password: str = Field(max_length=20)
    """
    gt: greater than
    ge: greater than or equal
    lt: less than
    le: less than or equal
    """

    class Config:
        schema_extra = {
            "default": {
                "id": 0,
                "name": "",
                "last_name": "",
                "nickname": "",
                "email": "",
                "password": "",
            }
        }