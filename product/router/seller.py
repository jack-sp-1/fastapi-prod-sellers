from fastapi import APIRouter
from typing import List
from passlib.context import CryptContext
from ..import models

pwd_cont = CryptContext(schemes=["bcrypt"],deprecated="auto")
router = APIRouter(tags=['seller'],prefix='/seller')
from ..schemas import Product,ProductDisp,Seller,DispSeller
from fastapi.params import Depends
from sqlalchemy.orm import Session
from  ..database import get_db
from .Login import get_current_user

@router.post('/',response_model=DispSeller)
def seller_add(request:Seller,db: Session=Depends(get_db)):
    hash_pasword = pwd_cont.hash(request.password)
    new_seller= models.Seller(username=request.username,email=request.email,password=hash_pasword)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller