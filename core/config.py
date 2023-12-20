import os
from dotenv import load_dotenv
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)



class Settings:
    PROJECT_NAME:str = "Intellect"
    PROJECT_VERSION: str = "1.0.0"
    
    
    POSTGRES_USER : str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER : str = os.getenv("POSTGRES_SERVER","localhost")
    POSTGRES_PORT : str = os.getenv("POSTGRES_PORT",5432)
    POSTGRES_DB : str = os.getenv("POSTGRES_DB","tdd")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
 
    SECRET_KEY :str = os.getenv("SECRET_KEY")   
    ALGORITHM = "HS256"                         
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    PERSONS_NUMBER:str = os.getenv("PERSONS_NUMBER")
    SERVER_NUMBER: str = os.getenv("SERVER_NUMBER")
    FIND_FACE_URL: str = os.getenv("FIND_FACE_URL")
    GET_IMAGE_URL: str = os.getenv("GET_IMAGE_URL")  
    
settings = Settings()