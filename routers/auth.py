from fastapi import APIRouter,Depends,HTTPException,Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel,Field
from ..models import Users
# from routers import todo
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi.security.http import HTTPBasicCredentials
from typing import Annotated,Optional
from jose import jwt,JWTError
from datetime import timedelta,datetime
from starlette import status
from ..database import sessiontrack
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates


route = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = '2a7a78a2e625ad3cc3ab66592e09195e614bfd7f96738762ed57b968185fe47f'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")





def get_db():
    db = sessiontrack()
    try:
        yield db
    finally:
        db.close()

    

db_dependency = Annotated[Session,Depends(get_db)]

template = Jinja2Templates(directory="TODOApp/templates")

### pages###

@route.get("/login-page")
def login_page(request:Request):
    return template.TemplateResponse('login.html',{'request':request})

@route.get("/register-page")
def register_page(request:Request):
    return template.TemplateResponse('register.html',{'request':request})



# user authentication check with db
def authenticate_user(username,password,db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hash_password):
        return False
    return user




class CreateUserRequest(BaseModel):
    username : str = Field(min_length=3)
    email : Optional[str] = Field(min_length=5)
    First_name : Optional[str] = Field(min_length=3)
    last_name : Optional[str] = Field(min_length=3)
    hash_password : str = Field(min_length=5)
    Phone_number : int 
    address : Optional[str] = Field(max_length=255,default='null')
    role : Optional[str] = Field(min_length=5)

# class User_Update(BaseModel):


class Token(BaseModel):
    access_token:str
    token_type:str


def create_acces_token(username:str,user_id:int,user_role:str,expire_delta:timedelta):
    encode = {'sub':username,'id':user_id,'user_role':user_role}
    expires = datetime.utcnow()+ expire_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

async def get_current_user(token:Annotated[str,Depends(oauth_bearer)]):
        
    # if not token:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    
    
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username:str = payload.get('sub')
        user_id: int = payload.get('id')
        # owner_id : int = payload.get('owner_id')
        user_role : str = payload.get('user_role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
        return {"username": username, "id": user_id,'user_role':user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    
@route.post("/")
async def create_user(db:db_dependency,create_user_request:CreateUserRequest):
    check_user = db.query(Users).filter(Users.username==create_user_request.username).first()
    if check_user:
        raise HTTPException(status.HTTP_409_CONFLICT,detail='User name already exist!!!')
    create_user_model = Users(
        username = create_user_request.username,
        email = create_user_request.email,
        First_name = create_user_request.First_name,
        last_name = create_user_request.last_name,
        hash_password = bcrypt_context.hash(create_user_request.hash_password),
        Phone_number = create_user_request.Phone_number,
        address = create_user_request.address,
        user_status = True,
        role = create_user_request.role
    )
    db.add(create_user_model)
    db.commit()
    #db.refresh(create_user_model)
    return RedirectResponse(url="/auth/login-page", status_code=status.HTTP_303_SEE_OTHER)



@route.get("/users")
async def get_user(db:db_dependency):
    all_user = db.query(Users).all()
    return all_user


@route.post("/token",response_model=Token)
async def login_request(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],
                        db:db_dependency):
    
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    
    token = create_acces_token(user.username,user.id,user.role,timedelta(minutes=5))
    return {'access_token':token,'token_type':'bearer'}

@route.put("/update_password")
async def update_user_password(db:db_dependency,id:int,user_data:CreateUserRequest):
    user = db.query(Users).filter(Users.id == id).first()
    print(user)
    if user is None:
        return {'message':'User not found','data':user_data}
    user.username = user_data.username
    user.hash_password = bcrypt_context.hash(user_data.hash_password)
    # user.email = user_data.email
    # user.First_name = user_data.First_name
    # user.last_name = user_data.last_name
    # user.role = user_data.role
    db.commit()
    db.refresh(user)


# @route.put("/Update_phone/{phone_number}")
# async def update_user_phone(userdb:db_dependency,phone_number:int,update_user:CreateUserRequest):

#     user_check = db.query(Users).filter(Users.id == update_user).first()
#     if user_check is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Username and id not found')
    
#     user_check.Phone_number = update_user.Phone_number
#     db.add(user_check)
#     db.commit()
#     return {'message':'Phone number updated successfully!!','data':user_check}


@route.delete("/delete_user/{username}/{user_id}")
async def delete_user(db:db_dependency,username:str,user_id:int):
    del_user = db.query(Users).filter(Users.username == username, Users.id == user_id).first()
    if not del_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User not found')
    db.delete(del_user)
    db.commit()
    # db.refresh(del_user)
    return {'Message':'User deleted succesfully!!','data':del_user}
