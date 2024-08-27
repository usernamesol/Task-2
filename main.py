from fastapi import FastAPI
from routes import users, files


app = FastAPI()
app.include_router(users.router)
app.include_router(files.router)
