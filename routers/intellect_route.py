from fastapi import APIRouter
from routers.login_route import get_current_user_from_token
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from db.models import User
from typing import List
from db.session import get_db
from schemas.intellect import FindFace
from db.repository.intellect import face_find

router = APIRouter()


@router.post("/findface")
def find_face(face:FindFace, user:User = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    data = face_find(face = face, user_id = user.id, db=db)
    return {
        "data"  : data["data"],
        "status": {
            "status_code":data["status_code"],
            "message"   :data["message"],
        }
    }