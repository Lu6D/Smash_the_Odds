# -*- coding: utf-8 -*-
"""
Created on 03/07/2023 13:40
@author: GiovanniMINGHELLI, LU6D
"""
import warnings

from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, Body, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
# from passlib.context import CryptContext
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
from fastapi import Form
from pydantic import BaseModel
from sources.data_pipeline.data_pipeline import *
from sources.data_pipeline.preprocessing.preprocessor import *
from sources.utils.utils import *
import joblib
import pickle
import csv
import os

# from config import USERS

warnings.filterwarnings("ignore")

project_path = get_root()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
# security = HTTPBasic()
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# users = {
#
#     "daniel": {
#         "username": "daniel",
#         "password": pwd_context.hash('datascientest'),
#     },
#     "john": {
#         "username": "john",
#         "password": pwd_context.hash('secret'),
#     },
#     "lucie": {
#         "username": "lucie",
#         "password": pwd_context.hash('ravie')
#     }
# }
#
#
# class UserCreate(BaseModel):
#     # user: Optional[str]= None
#     username: str
#     password: str
#
#
# class LoginRequest(BaseModel):
#     username: str
#     password: str


'''
@app.post("/login")
async def post_login(login_request: LoginRequest = Body(...)):
    username = login_request.username
    if not(users.get(username)):
        # User is not registered, redirect to user registration endpoint
        response = RedirectResponse(url="/user")
        return response
    elif not(pwd_context.verify(login_request.password, users[username]["password"])):
        # User is registered but provided incorrect password
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Basic"},
        )
    else:
        # User is registered and provided correct credentials, redirect to predict endpoint
        response = RedirectResponse(url="/status_test")
        return response
'''


@app.get("/")
def get_root():
    return {"status": 1}


@app.get("/status")
def get_status():
    return {"status": 1}


@app.get("/status_test")
async def get_status():
    # response = RedirectResponse(url="/predict")
    return {"status": 1}  # , "response": response}


@app.get('/predict/')
async def get_pred(match_id: int):
    model = joblib.load(get_last_model())
    match_info = get_match_info(match_id=match_id)
    try:
        data = global_transformer(match_info[['player1_id', 'player2_id']])
        return get_response(model=model, data=data)
    except TypeError:
        return match_info


'''


@app.post("/user")
async def add_user(user_info: UserCreate):

    new_user = {
        "username": user_info.username,
        "password": pwd_context.hash(user_info.password),
    }
    #vérification s'il n'est pas déjà existant dans le fichier users.csv

    if users.get(user_info.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )
    #update du dictionnaire
    users[user_info.username] = new_user
    #ajout d'une ligne dans le fichier users.csv
    with open(os.path.join(get_root(), 'users.csv'), mode="a", newline="") as csvfile:
        fieldnames = ["username", "password"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(new_user)
    return {"message": "User added successfully"}

@app.post("/logout")
async def logout_user(credentials: HTTPBasicCredentials = Depends(security)):
    # Here, you can perform any necessary cleanup or token/session invalidation logic.
    # For a simple logout, you can simply return a message.
    return {"message": "Logout successful"}
'''
