from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from dotenv import load_dotenv
import os

from routes import router

load_dotenv()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://cleric-extractor-client.onrender.com/"
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
        max_age=86400
    )
]

app = FastAPI(middleware=middleware)

app.include_router(router)