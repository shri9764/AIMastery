from fastapi import FastAPI,requests,Request
from .models import Base
from .database import engine
from TODOApp.routers import auth, todo, admin, users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

template = Jinja2Templates(directory="TODOApp/templates")

app.mount("/static",StaticFiles(directory="TODOApp/static"),name="static")

@app.get("/")
def test(request:Request):
    return template.TemplateResponse("home.html",{'request':request})


@app.get("/healthy")
async def health_check():
    return {'status': 'Healthy'}

# Including routers for different routes
app.include_router(auth.route)
app.include_router(todo.route)
app.include_router(admin.route)
app.include_router(users.route)

# Log the routes to verify registration
@app.on_event("startup")
async def on_startup():
    for route in app.routes:
        print(f"Route registered: {route.path}")













# from fastapi import FastAPI
# from .models import Base
# from .database import engine
# # from .models import *
# from TODOApp.routers import auth,todo,admin, users

# app = FastAPI()

# Base.metadata.create_all(bind=engine)

# @app.get("/healthy")
# async def health_check():
#     return {'status':'Healthy'}

# app.include_router(auth.route)
# app.include_router(todo.route)
# app.include_router(admin.route)
# app.include_router(users.route)
