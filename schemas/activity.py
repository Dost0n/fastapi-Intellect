from pydantic import BaseModel
from typing import Optional



class ActivityShow(BaseModel):
    id        : Optional[str]
    create_at : Optional[str]
    user_id   : Optional[str]

    class Config:
        orm_mode = True