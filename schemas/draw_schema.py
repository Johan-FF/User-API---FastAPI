from pydantic import BaseModel, Field
from typing import Optional

class DrawSchema(BaseModel):
    id: Optional[int] = None
    name: str = Field()
    details: str = Field()
    id_owner: int = Field()
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
                "details": "",
                "id_owner": 0,
            }
        }