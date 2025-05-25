from .utils import *
from ..routers.users import get_current_user,get_db
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_user


def test_users(test_user):
    response = client.get("/users/users")
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json()["username"] == "Shri"
    assert response.json()["email"] == "shri@gmail.com"
    assert response.json()["First_name"] == "Shrikrishna"
    assert response.json()["last_name"] == "Jagtap"
    assert response.json()["Phone_number"] == "9764424365"
    assert response.json()["address"] == "Pune"
    assert response.json()["role"] == "admin"

def test_change_password(test_user):
    response = client.put("/users/password", json={'password':'shri123',
                                                   'new_password':'shri@123'})
    
    assert response.status_code == status.HTTP_202_ACCEPTED

def test_change_password_invalid_current_password(test_user):
    response = client.put("/users/password", json={'password':'shri1234',
                                                   'new_password':'shri@123'})
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail':'Password is mismatched'}


def test_update_phone_number(test_user):
    new_phone = '7798869425'
    response = client.put(f"/users/Update_phone?phone_number={new_phone}")

    assert response.status_code == status.HTTP_202_ACCEPTED
    db = TestsessionLocal()
    record = db.query(Users).filter(Users.id == 1).first()
    assert record is not None
    assert record.Phone_number == new_phone
    assert response.json()['data']['Phone_Number'] == new_phone