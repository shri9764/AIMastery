import logging
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from ..database import sessiontrack
from ..models import Todos
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from starlette import status
from .auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

# Logging Configuration
logging.basicConfig(
    filename=r"C:\Users\ShrikrishnaJagtap\Desktop\Workspace\TODOApp\logs\todo.txt",
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

route = APIRouter(
    prefix="/todos",
    tags=['todos']
)

# Dependency injection
def get_db():
    db = sessiontrack()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
template = Jinja2Templates(directory="TODOApp/templates")

def redirect_to_login():
    redirect_to = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_to.delete_cookie(key='access_token')
    return redirect_to

#### PAGE ROUTES ####

@route.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        token = request.cookies.get('access_token')
        if not token:
            return RedirectResponse('/auth/login-page')

        user = await get_current_user(token)
        if user is None:
            return redirect_to_login()

        if user.get('user_role') == 'admin':
            todos = db.query(Todos).all()
        else:
            todos = db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

        # todos = db.query(Todos).filter(Todos.owner_id == user.get('id')).all()
        return template.TemplateResponse('todo.html', {'request': request, 'todos': todos, 'user': user})
    except Exception as e:
        logging.error(f"Error in render_todo_page: {e}")
        return redirect_to_login()

@route.get("/add-todo-page")
async def render_add_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get("access_token"))
        if user is None:
            return redirect_to_login()
        return template.TemplateResponse("add-todo.html", {"request": request, "user": user})
    except Exception as e:
        logging.error(f"Error in render_add_todo_page: {e}")
        return redirect_to_login()

@route.get("/edit/{todo_id}")
async def render_edit_todo(request: Request, db: db_dependency, todo_id: int):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        todo = db.query(Todos).filter(Todos.id == todo_id, Todos.owner_id == user.get('id')).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        return template.TemplateResponse("edit-todo.html", {"request": request, "todo": todo, "user": user})
    except Exception as e:
        logging.error(f"Error in render_edit_todo: {e}")
        return redirect_to_login()

#### API ENDPOINTS ####

class TodoRequest(BaseModel):
    title: str = Field(min_length=5)
    author: str = Field(min_length=3)
    description: str = Field(max_length=300)
    published_date: int = Field(gt=1970, le=2099)
    rating: int = Field(gt=0, le=5)
    price: int = Field(gt=100)
    owner_id: Optional[int] = None

@route.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed, Please login')

    if user.get('user_role') == 'admin':
        return db.query(Todos).all()
    else:
        return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()


@route.get("/todo-edit/{book_id}", status_code=status.HTTP_200_OK)
async def read_record_byId(user: user_dependency, db: db_dependency, book_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed, Please login')
    find_record = db.query(Todos).filter(Todos.id == book_id).first()
    if find_record is not None:
        return {
            'message': 'Record found',
            'data': {
                'id': find_record.id,
                'title': find_record.title,
                'author': find_record.author,
                'description': find_record.description,
                'published_date': find_record.published_date,
                'rating': find_record.rating,
                'price': find_record.price,
                'owner_id': find_record.owner_id
            }
        }
    raise HTTPException(status_code=404, detail='Record not found')

@route.post("/create_todo", status_code=status.HTTP_201_CREATED)
async def create_todo_record(user: user_dependency, db: db_dependency, todo_record: TodoRequest):
    try:
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')

        logging.info(f"Received todo_record: {todo_record}")
        todo_model = Todos(**todo_record.dict(exclude={"owner_id"}), owner_id=user.get('id'))
        db.add(todo_model)
        db.commit()
        db.refresh(todo_model)

        logging.info(f"Todo created successfully: {todo_model.title} (ID: {todo_model.id})")

        return {
            "Message": 'Record inserted successfully!!!',
            "Data": {
                'id': todo_model.id,
                'title': todo_model.title,
                'author': todo_model.author,
                'description': todo_model.description,
                'published_date': todo_model.published_date,
                'rating': todo_model.rating,
                'price': todo_model.price,
                'owner_id': todo_model.owner_id
            }
        }
    except Exception as e:
        logging.error(f"Error inserting todo: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@route.put("/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_record(user: user_dependency, db: db_dependency, todo_id: int, update_record: TodoRequest):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed, Please login')

    todo = db.query(Todos).filter(Todos.id == todo_id, Todos.owner_id == user.get('id')).first()
    if not todo:
        raise HTTPException(status_code=404, detail='Record not found')

    todo.title = update_record.title
    todo.author = update_record.author
    todo.description = update_record.description
    todo.rating = update_record.rating
    todo.price = update_record.price
    todo.published_date = update_record.published_date
    todo.owner_id = user.get('id')

    db.commit()
    logging.info(f"Todo updated successfully: {todo.title} (ID: {todo.id})")
    return {"message": "Record updated successfully"}

@route.delete("/delete/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_record(user: user_dependency, db: db_dependency, todo_id: int):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed, Please login')

    result = db.query(Todos).filter(Todos.id == todo_id).first()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found!!!")

    if result.owner_id != user.get('id'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Failed, Could not delete another user's records")

    db.delete(result)
    db.commit()

    logging.info(f"Todo deleted: {result.title} (ID: {result.id}) by user {user.get('id')}")

    return {
        'message': "Record deleted successfully",
        "data": {
            'id': result.id,
            'title': result.title,
            'author': result.author,
            'description': result.description,
            'published_date': result.published_date,
            'rating': result.rating,
            'price': result.price,
            'owner_id': result.owner_id
        }
    }
