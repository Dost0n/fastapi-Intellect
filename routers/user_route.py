from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from db.session import get_db
from typing import List
from db.models import User
from schemas.users import UserCreate, UserShow, UserUpdate
from db.repository.user import create_admin, list_users, create_user, retreive_user, update_user, delete_user
from routers.login_route import get_current_user_from_token

router = APIRouter()


@router.get("/all", response_model=List[UserShow])
def get_all_users(db:Session = Depends(get_db), current_user:User = Depends(get_current_user_from_token)):
    if current_user.is_staff:
        users = list_users(db=db)
        return users
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not permitted!!!!")



@router.post("/createusers", status_code = status.HTTP_201_CREATED )
def create_users(user: UserCreate, db: Session = Depends(get_db), current_user:User = Depends(get_current_user_from_token)):
    if current_user.is_staff:
        db_username = db.query(User).filter(User.username == user.username).first()
        if db_username is not None:
            return HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
                detail = "This username address already exist")
        user = create_user(user=user, db=db)
        return {
        "username":f"{user.username}",
        "office":f"{user.office}",
        "is_staff":f"{user.is_staff}",
    }
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "You are not permitted!!!")


@router.post("/createadmin", status_code = status.HTTP_201_CREATED )
def create_admins(user: UserCreate, db: Session = Depends(get_db)):
    users = list_users(db=db)
    if len(users)==0:
        user = create_admin(user=user, db=db)
        return {
        "username":f"{user.username}",
        "office":f"{user.office}",
        "is_staff":f"{user.is_staff}",
    }
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "You are not permitted!!!")



@router.get("/{user_id}",response_model=UserShow)
def read_user(user_id:str, db:Session = Depends(get_db), current_user:User = Depends(get_current_user_from_token)):
    if current_user.is_staff:
        user = retreive_user(user_id=user_id, db=db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with this id {user_id} does not exist")
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not permitted!!!!")



@router.put("/update/{user_id}") 
def update_users(user_id:str, user: UserUpdate, db: Session = Depends(get_db), current_user:User = Depends(get_current_user_from_token)):
    if current_user.is_staff:
        message = update_user(user_id=user_id, user=user, db=db)
        if not message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with id {user_id} not found")
        return {"msg":"Successfully updated data."}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not permitted!!!!")



@router.delete("/delete/{user_id}")
def delete_users(user_id:str, db: Session = Depends(get_db), current_user:User = Depends(get_current_user_from_token)):
    if current_user.is_staff:
        user = retreive_user(user_id=user_id,db=db)
        if not user:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with this id {user_id} does not exist")
        if user:
            delete_user(user_id=user_id,db=db)
            return {"detail": "Successfully deleted."} 
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not permitted!!!!")