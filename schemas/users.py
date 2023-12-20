from pydantic import BaseModel
from typing import Optional



class UserCreate(BaseModel):
    id         :Optional[str]
    username   :Optional[str]
    password   :Optional[str]
    office     :Optional[str]
    is_staff   :Optional[bool]
    
    class Config:
        orm_mode = True
        schema_extra = {
            'example' :{
                'username'   :'user',
                'password'   :'123',
                'office'     :'Darxon',
                'is_staff'   :False,
            }
        }


class AdminCreate(BaseModel):
    id         :Optional[str]
    username   :Optional[str]
    password   :Optional[str]
    office     :Optional[str]
    is_staff   :Optional[bool]
    
    class Config:
        orm_mode = True
        schema_extra = {
            'example' :{
                'username'   :'user',
                'password'   :'123',
                'office'     :'Darxon',
                'is_staff'   : True,
            }
        }



class UserShow(BaseModel):
    id         :Optional[str]
    username   :Optional[str]
    office     :Optional[str]
    is_staff   :Optional[bool]

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username   :Optional[str]
    password   :Optional[str]
    office     :Optional[str]
    is_staff   :Optional[bool]

    class Config:
        orm_mode = True

