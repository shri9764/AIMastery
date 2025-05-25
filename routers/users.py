from pydantic import BaseModel,Field
from fastapi import APIRouter,Depends,HTTPException,Path,Query
from ..database import sessiontrack
from ..models import Todos,Users
from typing import Annotated,Optional
from sqlalchemy.orm import Session
from starlette import status
from .auth import get_current_user
from passlib.context import CryptContext


route = APIRouter(
    prefix='/users',
    tags=['users']
)




def get_db():
    db = sessiontrack()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')


class user_verification(BaseModel):
    password : str
    new_password : str


@route.get('/users',status_code=status.HTTP_202_ACCEPTED)
async def get_user(user:user_dependency,
                   db:db_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Authentication failed')
    
    find_user= db.query(Users).filter(Users.id == user.get('id')).first()
    return find_user


@route.put('/password',status_code=status.HTTP_202_ACCEPTED)
async def update_user_password(user:user_dependency,db:db_dependency,user_verification:user_verification):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Authentication failed')
    
    user_find = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password,user_find.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Password is mismatched')
    
    user_find.hash_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_find)
    db.commit()
    return {'message':'Password updated successfully!!!'}


@route.put("/Update_phone",status_code=status.HTTP_202_ACCEPTED)
async def update_user_phone(user:user_dependency,db:db_dependency,phone_number:str):

    user_check = db.query(Users).filter(Users.username == user.get('username')).first()
    if user_check is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Username and id not found')
    
    user_check.Phone_number = phone_number
    db.add(user_check)
    db.commit()
    return {'message':'Phone number updated successfully!!','data':{'username':user_check.username,
                                                                    'Phone_Number':user_check.Phone_number}}

