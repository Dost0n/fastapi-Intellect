from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from db.session import get_db
from typing import List
from db.models import Activity, User
from schemas.activity import ActivityShow
from db.repository.activity import list_activity, retreive_activity, delete_activity
from routers.login_route import get_current_user_from_token

router = APIRouter()


@router.get("/all", response_model=List[ActivityShow])
def get_all_activities(db:Session = Depends(get_db), current_user:User = Depends(get_current_user_from_token)):
    if current_user.is_staff:
        activities = list_activity(db=db)
        return activities
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not permitted!!!!")


@router.get("/{activity_id}",response_model=ActivityShow)
def read_activity(activity_id:str, db:Session = Depends(get_db), current_user:User = Depends(get_current_user_from_token)):
    if current_user.is_staff:
        activity = retreive_activity(activity_id=activity_id, db=db)
        if not activity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Activity with this id {activity_id} does not exist")
        return activity
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not permitted!!!!")


@router.delete("/delete/{activity_id}")
def delete_activities(activity_id:str, db: Session = Depends(get_db), current_user:User = Depends(get_current_user_from_token)):
    if current_user.is_staff:
        activity = retreive_activity(activity_id=activity_id,db=db)
        if not activity:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Activity with this id {activity_id} does not exist")
        if activity:
            delete_activity(activity_id=activity_id,db=db)
            return {"detail": "Successfully deleted."} 
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not permitted!!!!")