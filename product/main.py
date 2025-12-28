from fastapi import  FastAPI, HTTPException
from pydantic import  BaseModel
from .import models
from .database import engine
from fastapi import status

from fastapi.params import Depends
from sqlalchemy.orm import Session
from .schemas import Product,ProductDisp,Seller,DispSeller

from .database import SessionLocal
from typing import List
from passlib.context import CryptContext
from .router import product,seller,Login
from  .database import get_db

pwd_cont = CryptContext(schemes=["bcrypt"],deprecated="auto")
from .router.Login import get_current_user

#,current_user:Seller=Depends(get_current_user)
        

        

###
app = FastAPI(
    title="Products and sellers",
    description="for prod and sellers",
    terms_of_service="http://www.google.com",
    contact=
    {'developer name':"vas"},
    license_info={'name':"vas","url":"http://www.google.com"}
)
app.include_router(seller.router)
app.include_router(Login.loginrouter)

@app.post('/product',status_code=status.HTTP_201_CREATED,tags=['products'])
def add(request: Product,db: Session=Depends(get_db)):
    new_product= models.Product(name=request.name,description=request.description,price=request.price,seller_id=1)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request

#it returns a list

@app.get('/products',response_model=List[ProductDisp])
def products(db: Session=Depends(get_db),current_user:Seller=Depends(get_current_user)):
    products = db.query(models.Product).all()
    return products

#it returns a dict
@app.get('/product/{id}')
def product(id,db: Session=Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id==id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found")
    return product

@app.delete('/product/{id}')
def product(id,db: Session=Depends(get_db)):
    db.query(models.Product).filter(models.Product.id==id).delete(synchronize_session=False)
    db.commit()
    return 'deletion done'

@app.put('/product/{id}')
def update(id,request: Product,db: Session=Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id==id)
    if not product.first():
        pass
    product.update(request.model_dump())
    db.commit()
    return 'product update done'


###

models.Base.metadata.create_all(engine)
'''
@app.post('/productnew')
def add(request:Product):
    return request
'''