from pydantic import BaseModel
from typing import Optional



class LogShow(BaseModel):
    id        : Optional[str]
    photo_id  : Optional[str]
    persent   : Optional[str]
    create_at : Optional[str]
    user_id   : Optional[str]

    class Config:
        orm_mode = True