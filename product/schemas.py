#pydantic  models
from pydantic import BaseModel

from typing import Optional

class Product(BaseModel):
    name:str
    description:str
    price:int
    
class ProductDisp(BaseModel):
    name:str
    description:str
    class Config:
        from_attributes = True
        
class Seller(BaseModel):
    username:str
    email:str
    password:str
    
class DispSeller(BaseModel):
    username:str
    email:str
    class Config:
        from_attributes = True            


class Login(BaseModel):
    username: str
    password: str            


class Token(BaseModel):
    access_token:str
    token_type:str
    
class  TokenData(BaseModel):
    username:Optional[str]  = None        