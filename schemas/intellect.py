from pydantic import BaseModel,Extra
from typing import Optional



class FindFace(BaseModel):
    image      :Optional[str]

    class Config:
        extra = Extra.forbid