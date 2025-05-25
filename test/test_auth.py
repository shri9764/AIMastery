from .utils import *
from ..routers.auth import get_db,authenticate_user,create_acces_token,SECRET_KEY,ALGORITHM,get_current_user
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException

app.dependency_overrides[get_db] = override_get_db

def test_authentication_user(test_user):
    db = TestsessionLocal()

    authenticate = authenticate_user(test_user.username,'shri123',db)
    assert authenticate is not None
    assert authenticate.username == test_user.username

def test_authentication_not_user(test_user):
    db = TestsessionLocal()

    authenticate = authenticate_user('shri','shri123',db)
    assert authenticate is False
    # assert authenticate.username != test_user.username

def test_authentication_user_password(test_user):
    db = TestsessionLocal()

    authenticate = authenticate_user('Shri','shri1232',db)
    assert authenticate is False

def test_access_token():
    username = 'testuser'
    user_id = 1
    role = 'admin'
    expire_delta = timedelta(minutes=5)

    token = create_acces_token(username,user_id,role,expire_delta)

    decoded_token = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM],options={'verify_sign': False})

    assert decoded_token['sub'] == 'testuser'
    assert decoded_token['id'] == 1
    assert decoded_token['user_role'] == 'admin'


@pytest.mark.asyncio
async def test_current_user():
    encode = {'sub':'testuser','id':1,'user_role':'admin'}
    token = jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
    user = await get_current_user(token=token)

    assert user == {'username' :'testuser','id':1,'user_role':'admin'}


@pytest.mark.asyncio
async def test_current_user_not():
    encode = {'role':'user'}
    token = jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == 'Could not validate user'