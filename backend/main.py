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
    os.environ.get("DOMAIN_URL")
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=86400
)

app.include_router(router)