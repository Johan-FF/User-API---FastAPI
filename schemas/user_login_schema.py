from pydantic import BaseModel, Field

class UserLoginSchema(BaseModel):
    email: str = Field(max_length=30)
    password: str = Field(max_length=20)

    class Config:
        schema_extra = {
            "default": {
                "email": "",
                "password": "",
            }
        }