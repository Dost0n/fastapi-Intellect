from sqlalchemy.orm import Session
from db.models import Activity
import datetime, uuid
from fastapi import Depends
from db.session import get_db


def list_activity(db : Session):
    activities = db.query(Activity).all()
    return activities


def create_activity(id_user, db:Session):
    activity_date = str(datetime.datetime.now())
    activity_id   = str(uuid.uuid1())
    activity_object = Activity(
        id        = activity_id,
        user_id   = id_user,
        create_at = activity_date,
    )
    db.add(activity_object)
    db.commit()
    db.refresh(activity_object)
    return 1


def retreive_activity(activity_id:str, db:Session):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    return activity



def delete_activity(activity_id:str, db: Session):
    existing_activity = db.query(Activity).filter(Activity.id == activity_id)
    if not existing_activity.first():
        return 0
    existing_activity.delete(synchronize_session=False)
    db.commit()
    return 1