from sqlalchemy.orm import Session
from db.models import Log
import datetime, uuid
from fastapi import Depends
from db.session import get_db


def list_logs(db : Session):
    logs = db.query(Log).all()
    return logs


def create_log(imageId, id_user, photo_persent, db:Session):
    log_date = str(datetime.datetime.now())
    log_id   = str(uuid.uuid1())
    log_object = Log(
        id         = log_id,
        photo_id   = imageId,
        user_id    = id_user,
        persent    = photo_persent,
        create_at  = log_date,
    )
    db.add(log_object)
    db.commit()
    db.refresh(log_object)
    return 1


def retreive_log(log_id:str, db:Session):
    log = db.query(Log).filter(Log.id == log_id).first()
    return log



def delete_log(log_id:str, db: Session):
    existing_log = db.query(Log).filter(Log.id == log_id)
    if not existing_log.first():
        return 0
    existing_log.delete(synchronize_session=False)
    db.commit()
    return 1