from sqlalchemy.orm import Session
from schemas.intellect import FindFace
import datetime, uuid
from core.config import settings
import requests
import base64
from db.repository.log import create_log

def face_find(face = FindFace, user_id = str, db=Session):
    URL = settings.FIND_FACE_URL
    payload = {
        "server_id"  : settings.SERVER_NUMBER,
        "findPersons": int(settings.PERSONS_NUMBER),
        "image"      : f"{face.image}"
    }
    data = []
    try:
        response = requests.post(URL, json = payload)
        jsonData = response.json()
        FaceList = jsonData['FaceList']
        for i in FaceList:
            PersonList = i.get('PersonList')
            for j in PersonList:
                person = {}
                person['name']     = j.get('Name')
                person['surname']  = j.get('Surname')
                person['patronym'] = j.get('Patronymic')
                person['imageId']  = j.get('ImageId')
                person['sim']      = j.get('Sim')
                person['image']    = getImage(person['imageId'])
                create_log(person['imageId'], user_id, person['sim'], db=db)
                data.append(person)
        status_code = response.status_code
        message     = "SUCCESS"
    except requests.exceptions.RequestException:
        status_code = 500
        message     = "SERVER CONNECTION ERROR"
    data = sorted(data, key=lambda i:i['sim'], reverse=True)
    return {
        "data"       : data,
        "status_code": status_code,
        "message"    : message
        }


def getImage(imageId):
    URL = f"{settings.GET_IMAGE_URL}/{settings.SERVER_NUMBER}/{imageId}"
    response = requests.get(URL)
    result   = base64.b64encode(response.content).decode()
    return result
