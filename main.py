from fastapi import FastAPI
from pydantic import BaseModel
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

config = context.config

fileConfig(config.config_file_name)

app = FastAPI()

"""
username
email
created_at
updated_at
"""
class User(BaseModel):
    username: str
    email: str

"""
title
type: ChoiceField (e.g. text or image)
is_add_choices_active
is_voting_active
created_by
"""
class Poll(BaseModel):
    title: str
    type: str
    is_add_choices_active: bool
    is_voting_active: bool
    created_by: int

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/polls")
async def root():
    return {"polls": "Hello World"}

@app.get("/users")
async def root():
    return {"users": "Hello World"}

@app.post("/users")
async def create_user(user: User):
    return user

@app.post("/polls")
async def create_user(poll: Poll):
    return poll