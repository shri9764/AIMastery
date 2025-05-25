from sqlalchemy import create_engine
from ..routers.auth import get_db,authenticate_user,create_acces_token,SECRET_KEY,ALGORITHM
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from ..database import Base
from ..models import Todos,Users
from ..routers.auth import bcrypt_context
from ..main import app
import pytest
from datetime import timedelta,datetime
from jose import jwt



SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={'check_same_thread':False},
                       poolclass=StaticPool)

TestsessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)


def override_get_db():
    db = TestsessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_user():
    return {'username': 'Shri', 'id': 1, 'user_role': 'admin'}





client = TestClient(app)


@pytest.fixture
def test_todo():
    db = TestsessionLocal()
    db.query(Todos).delete()  # Ensure the table is clean before inserting new data.
    todo = Todos(id=1, title="Gen AI", 
                 author="IBM org", 
                 description="AI career", 
                 published_date='2001', 
                 rating=5, 
                 price=10000, 
                 owner_id=1)
    db.add(todo)
    db.commit()
    yield todo

    # with engine.connect() as conn:
    #     conn.execute("Delete * from todo;")
    #     conn.commit()


@pytest.fixture
def test_user():
    db = TestsessionLocal()
    db.query(Users).delete()

    user = Users(
  username = "Shri",
  email = "shri@gmail.com",
  First_name = "Shrikrishna",
  last_name = "Jagtap",
  hash_password = bcrypt_context.hash("shri123"),
  Phone_number = "9764424365",
  address = "Pune",
  role = "admin")
    
    
    db.add(user)
    db.commit()
    yield user

