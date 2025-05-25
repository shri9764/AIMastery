from .utils import *
from ..routers.admin import get_current_user,get_db
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_user



def test_admin_get_all_record(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'id': 1,
        'title': "Gen AI",
        'author': "IBM org",
        'description': "AI career",
        'published_date': '2001',
        'rating': 5,
        'price': 10000,
        'owner_id': 1}]


def test_Not_admin_get_all_record(test_todo):

    def overide_non_admin():
        return {'username':'Shri','id':1,'user_role':'user'}

    
    app.dependency_overrides[get_current_user] = overide_non_admin

    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail':"You don't have admin rights!!"}

def test_admin_delete_record(test_todo):
    def override_admin():
        return {'username': 'Shri', 'id': 1, 'user_role': 'admin'}

    app.dependency_overrides[get_current_user] = override_admin

    response = client.delete("/admin/delete/1")
    assert response.status_code == status.HTTP_200_OK
    db = TestsessionLocal()
    record = db.query(Todos).filter(Todos.id == 1).first()
    assert record is None

def test_admin_delete_no_record(test_todo):
    def override_admin():
        return {'username': 'Shri', 'id': 1, 'user_role': 'admin'}

    app.dependency_overrides[get_current_user] = override_admin

    response = client.delete("/admin/delete/111")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail' : "Record not found!!"}