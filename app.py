from fastapi import FastAPI, Form, HTTPException,Depends,status,Request
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
app= FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
models.Base.metadata.create_all(bind=engine)
# This line will create all of the tables and columns in postgres
# class PostBase(BaseModel):
#     title: str
#     content: str
#     user_id: int
# class UserBase(BaseModel):
#     username: str
   
def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

# db_dependency= Annotated[Session,Depends(get_db)]
@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.id.desc())
    return templates.TemplateResponse("index.html", {"request": request, "users": users})

@app.post("/add")
async def add(request: Request, name: str = Form(...), position: str = Form(...), office: str = Form(...), db: Session = Depends(get_db)):
    print(name)
    print(position)
    print(office)
    users = models.User(name=name, position=position, office=office)
    db.add(users)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/addnew")
async def addnew(request: Request):
    return templates.TemplateResponse("addnew.html", {"request": request})

@app.get("/edit/{user_id}")
async def edit(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return templates.TemplateResponse("edit.html", {"request": request, "user": user})

@app.post("/update/{user_id}")
async def update(request: Request, user_id: int, name: str = Form(...), position: str = Form(...), office: str = Form(...), db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.id == user_id).first()
    users.name = name
    users.position = position
    users.office = office
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete/{user_id}")
async def delete(request: Request, user_id: int, db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(users)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)
# @app.get("/")
# def home(request:Request, db: Session = Depends(get_db)):
#     todos = db.query(models.Todo).all()
#     return templates.TemplateResponse("base.html",{"request": request, "todo_list": todos})

# @app.post("/add")
# def add(request: Request,title: str = Form(...), db: Session = Depends(get_db)):
#     new_todo = models.Todo(title=title)
#     db.add(new_todo) 
#     db.commit()
    
#     url= app.url_path_for("home")
#     return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

# @app.get("/update/{todo_id}")
# def update(request: Request,todo_id: int,title: str = Form(...), db: Session = Depends(get_db)):
#     new_todo = models.Todo(title="sutichar")
#     todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
#     # todo.complete = not todo.complete 
#     todo.title = new_todo
#     db.commit()
    
#     url= app.url_path_for("home")
#     return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)
# @app.get("/delete/{todo_id}")
# def delete(request: Request,todo_id: int, db: Session = Depends(get_db)):
#     todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
#     db.delete(todo) 
#     db.commit()
    
#     url= app.url_path_for("home")
#     return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)
    
    
         
    
    
