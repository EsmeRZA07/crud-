from fastapi import APIRouter
from config.db import conn
from models.user import users
from schemas.user import User
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()
@user.get('/users')
def get_users():
    return conn.execute(users.select()).mappings().fetchall()

@user.post('/users')
def create_users(user:User):
    new_user = {"name": user.name,"email":user.email, "password": f.encrypt(user.password.encode("utf-8"))}
    conn.execute(users.insert().values(new_user))
    conn.commit()
   
@user.get('/users/{id}')
def  get_id_users(id: str):
    return conn.execute(users.select().where(users.c.id == id)).mappings().first()
     
@user.delete("/users/{id}")
def delete_users(id:str):
    conn.execute(users.delete().where(users.c.id == id)).mappings()
    conn.commit()
    
@user.put("/users/{id}")
def update_users(id:str, user: User):
    conn.execute(users.update().values(name = user.name, email = user.email, password = f.encrypt(user.password.encode("utf-8"))).where(users.c.id == id))
    