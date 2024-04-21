from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from routes import router

load_dotenv()

app = FastAPI()

#app.mount("/logs", StaticFiles(directory="logs"), name="logs")
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://cleric-extractor-client.onrender.com/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Access-Control-Allow-Methods"],
    max_age=86400
)

app.include_router(router)