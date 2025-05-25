# import TODOApp.models as models
from .database import Base
from sqlalchemy import Column,Integer,Boolean,String,ForeignKey

# User Model
class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique=True)
    email = Column(String,unique=True)
    First_name = Column(String)
    last_name = Column(String)
    hash_password = Column(String)
    Phone_number = Column(String)
    address = Column(String(),nullable=True)
    user_status = Column(Boolean)
    role = Column(String)


class Todos(Base):
    __tablename__ = 'todo'

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String(200),unique=True) 
    author = Column(String(100))
    description =Column(String(300))
    published_date = Column(String(20))
    rating = Column(Integer)
    price = Column(Integer)
    owner_id = Column(Integer,ForeignKey('users.id'))