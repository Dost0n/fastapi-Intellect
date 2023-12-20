from sqlalchemy.orm import Session
from db.models import User
from schemas.users import UserCreate, UserShow, AdminCreate,UserUpdate
import datetime, uuid
from db.hashing import Hasher


def list_users(db : Session):
    users = db.query(User).all()
    return users


def create_user(user: UserCreate, db: Session):
    user_date = str(datetime.datetime.now())
    user_id   = str(uuid.uuid1())
    user_object = User(
        id         = user_id,
        username   = user.username,
        password   = Hasher.get_password_hash(user.password),
        office     = user.office,
        create_at  = user_date,
        is_staff   = user.is_staff,
    )
    db.add(user_object)
    db.commit()
    db.refresh(user_object)
    return user_object

def create_admin(user: AdminCreate, db: Session):
    user_date = str(datetime.datetime.now())
    user_id   = str(uuid.uuid1())
    user_object = User(
        id         = user_id,
        username   = user.username,
        password   = Hasher.get_password_hash(user.password),
        office     = user.office,
        create_at  = user_date,
        is_staff   = user.is_staff,
    )
    db.add(user_object)
    db.commit()
    db.refresh(user_object)
    return user_object


def retreive_user(user_id:str, db:Session):
    user = db.query(User).filter(User.id == user_id).first()
    return user


def update_user(user_id:str, user: UserUpdate, db: Session):
    existing_user = db.query(User).filter(User.id == user_id)
    user.password = Hasher.get_password_hash(user.password)
    if not existing_user.first():
        return 0
    existing_user.update(user.__dict__)
    db.commit()
    return 1


def delete_user(user_id:str, db: Session):
    existing_user = db.query(User).filter(User.id == user_id)
    if not existing_user.first():
        return 0
    existing_user.delete(synchronize_session=False)
    db.commit()
    return 1