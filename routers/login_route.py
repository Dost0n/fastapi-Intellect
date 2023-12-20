from fastapi import Depends,APIRouter
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi import status,HTTPException
from db.session import get_db
from db.hashing import Hasher
from schemas.token import Token
from db.repository.login import get_user
from db.models import User
from core.security import create_access_token
from core.config import settings
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from schemas.login import LoginSchema
from db.repository.activity import create_activity
router = APIRouter()


def authenticate_user(username: str, password: str,db: Session):
    user = get_user(username=username,db=db)
    if not user:
        return False
    if not Hasher.verify_password(password, user.password):
        return False
    return user



@router.post("/token")
def login_for_access_token(login: LoginSchema, db: Session= Depends(get_db)):
    user = authenticate_user(login.username, login.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            
        )
    create_activity(user.id, db)
    user_role = user.is_staff
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "is_superuser":user_role,"token_type": "bearer"}



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/token")



def get_current_user_from_token(token: str = Depends(oauth2_scheme),db: Session=Depends(get_db)): 
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW_Authenticate":"Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username=username,db=db)
    if user is None:
        raise credentials_exception
    return user