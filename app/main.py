from typing import Optional, List
from fastapi import Body, FastAPI
from pydantic import BaseSettings
from . import models
from .database import engine
from .routers import posts, users, auth, votes
from .config import settings

from fastapi.middleware.cors import CORSMiddleware


# This is telling which hashing algorithm to use.

# The following line creates tables from models, but only when there are no tables in a database.
# models.Base.metadata.create_all(bind=engine)

# For more flexible behavior use alembic. Commands are as follows:
# To create each 'migration' manualy, first create a revision (migration) file with alembic revision -m "Message" command.
# Next In def upgrade() and def downgrade() tell alembic what to do in the database.
# Use alembic upgrade + id of revision, or head (to implement the latest revision) for creating tables in the database.
# For removing things from database use alembic downgrade + id of the revision to which you downgrade.


app = FastAPI()

origins = ["https://www.google.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
