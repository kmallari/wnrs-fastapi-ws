from fastapi import Depends, FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from src.db import models
from src.db.db import engine
from src.routers import rest, socket

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# implement cors
origins = [
    "http://localhost:5173",  # For SvelteKit development server
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(rest.router)
app.include_router(socket.router)
