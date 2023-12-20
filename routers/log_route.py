from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from db.session import get_db
from typing import List
from db.models import Log, User
from schemas.log import LogShow
from db.repository.log import list_logs, create_log, retreive_log, delete_log
from routers.login_route import get_current_user_from_token

router = APIRouter()



@router.get("/all", response_model=List[LogShow])
def get_all_logs(db:Session = Depends(get_db), current_user:User = Depends(get_current_user_from_token)):
    if current_user.is_staff:
        logs = list_logs(db=db)
        return logs
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not permitted!!!!")


@router.get("/{log_id}",response_model=LogShow)
def read_log(log_id:str, db:Session = Depends(get_db), current_user:User = Depends(get_current_user_from_token)):
    if current_user.is_staff:
        log = retreive_log(log_id=log_id, db=db)
        if not log:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Log with this id {log_id} does not exist")
        return log
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not permitted!!!!")


@router.delete("/delete/{log_id}")
def delete_logs(log_id:str, db: Session = Depends(get_db), current_user:User = Depends(get_current_user_from_token)):
    if current_user.is_staff:
        log = retreive_log(log_id=log_id,db=db)
        if not log:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Log with this id {log_id} does not exist")
        if log:
            delete_log(log_id=log_id,db=db)
            return {"detail": "Successfully deleted."} 
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not permitted!!!!")