from pydantic import BaseModel,Field
from fastapi import APIRouter,Depends,HTTPException,Path,Query,Request
from ..database import sessiontrack
from ..models import Todos,Users
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from .auth import get_current_user
from ..routers.todo import redirect_to_login
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse



route = APIRouter(
    prefix='/admin',
    tags=['admin']
)




def get_db():
    db = sessiontrack()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

template = Jinja2Templates(directory="TODOApp/templates")


@route.get('/todo', status_code=status.HTTP_200_OK)
async def admin_role_user(user:user_dependency,db:db_dependency):
    if user is None or user.get('user_role','').casefold() != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have admin rights!!")
        
    all_book= db.query(Todos).all()
    return all_book
# # Read admin dashboard
# @route.get("/admin")
# async def admin_dashboard(request: Request, db: db_dependency):
#     user = await get_current_user(request.cookies.get('access_token'))
#     if not user or user.get('user_role') != 'admin':
#         return redirect_to_login()

#     todos = db.query(Todos).all()
#     return template.TemplateResponse('admin-dashboard.html', {'request': request, 'todos': todos, 'user': user})

@route.get("/users")
async def admin_all_users(user:user_dependency,db:db_dependency):
    if user is None or user.get('user_role','').casefold() != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Don't have admin rights")
    # return db.query(Todos).all()
    return db.query(Users).all()

@route.delete('/delete/{todo_id}', status_code=status.HTTP_200_OK)
async def delete_record_by_admin(
    todo_id: int,
    user: user_dependency,
    db: db_dependency
):
    if user is None or user.get('user_role', '').casefold() != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have admin rights!!"
        )

    record = db.query(Todos).filter(Todos.id == todo_id).first()
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found!!"
        )

    db.delete(record)
    db.commit()
    return {"Message": "Record deleted successfully!!!", "Data": {
        "id": record.id,
        "title": record.title
    }}
