from  fastapi import APIRouter,status,HTTPException
from ..schemas import Login,TokenData,Token
from  ..database import get_db
from fastapi.params import Depends
from sqlalchemy.orm import Session
from ..import models
from passlib.context import CryptContext
loginrouter = APIRouter()
pwd_cont = CryptContext(schemes=["bcrypt"],deprecated="auto")
from datetime import datetime,timedelta
from jose import jwt
from jose.exceptions import JWTError
SECRET_KEY = '12222222222222222222222222222'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Login")

def get_current_user(token:str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "invalidauth",
        headers = {'WWW-Authenticate':"Bearer"}
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

def generate_token(data:dict):
    if not isinstance(data,dict):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,)
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encoded_jwt

@loginrouter.post('/Login/')
def login(request:OAuth2PasswordRequestForm= Depends(),db: Session=Depends(get_db)):
    user = db.query(models.Seller).filter(models.Seller.username==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="username not found") 
    #hash_pasword = pwd_cont.hash(request.password)
    if not pwd_cont.verify(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalied password")
    access_token = generate_token(
        data={"sub":user.username})
    
    return {"access_token":access_token,"token_type":"bearer"}
    #return request