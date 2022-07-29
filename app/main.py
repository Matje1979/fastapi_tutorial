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
# my_posts = [
#     {"id": 1, "title": "Post 1", "content": "Hello world"},
#     {"id": 2, "title": "Post 2", "content": "Hello world"},
#     {"id": 3, "title": "Post 3", "content": "Hello Moon"},
# ]
# cursor_factory gives the names of the columns.
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fastapi_db",
#             user="damir",
#             password="@DamirSymphony1979",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("Database connection was successfull!")
#         break
#     except Exception as error:
#         print(f"Connecting to db failed because of the following error: {error}. ")

# time.sleep(2)


# @app.get("/")
# async def index():
#     return {"message": "New Data"}


# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     # Query fancy, SQLAlchemy way.
#     # posts = db.query(models.Post).all()
#     posts = db.query(
#         models.Post
#     ).all()  # this creates a query, but to run a query we must add something like .all().
#     return {"data": "mata"}


# @app.get("/posts")
# def get_posts(db: Session = Depends(get_db), response_model=List[schemas.Post]):
#     # Query oldfashioned, raw SQL way.
#     posts = db.query(models.Post).all()
#     return posts


# def find_post(id):
#     for p in my_posts:
#         print(p["id"], id)
#         if (p["id"]) == id:
#             return p
#     return None


# Be careful, bellow route matches also "/posts/details/..." or similar. Solution: order of routes is important.
# @app.get("/posts/{id}")
# def get_post(id: int, response: Response, db: Session = Depends(get_db)):

#     post = db.query(models.Post).filter(models.Post.id == id).first()
#     # cursor.execute("""SELECT * FROM post WHERE id = %s""" % (str(id)))
#     # post = cursor.fetchone()
#     if not post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Requested post not found"
#         )
#     return {"data": post}


# @app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):

# new_post = models.Post(
#     title=post.title, content=post.content, published=post.published
# )

# The following is the same as the lines above:
# new_post = models.Post(**post.dict())
# db.add(new_post)
# db.commit()
# db.refresh(new_post)
# We don't use f string in execute statement because that would expose us to sql injection attacks.
# cursor.execute(
#     """ INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
#     (post.title, post.content, post.published),
# )
# fetchall() for all, fetchone() for one.
# new_post = cursor.fetchone()
# Created post needs to be saved (commited) in the database.
# conn.commit()
# print(type(post))
# post_dict = post.dict()
# post_dict["id"] = randrange(1, 1000000)
# my_posts.append(post_dict)
# print(my_posts)
# print(new_post)
# return new_post

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int, db: Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == id).first()
#     # cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""" % (str(id)))
#     # deleted_post = cursor.fetchone()
#     if post == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with the id of {id} does not exist",
#         )
#     else:
#         post.delete(synchronize_session=False)
#         db.commit()
# conn.commit()
# index = find_index_post(id)
# if index == None:
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail=f"Post with the ide {id} does not exist",
#     )
# my_posts.pop(index)
# return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}")
# def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
#     update_post = db.query(models.Post).filter(models.Post.id == id)
#     post_for_update = update_post.first()
# cursor.execute(
#     """UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
#     (
#         post.title,
#         post.content,
#         post.published,
#         str(id),
#     ),
# )
# updated_post = cursor.fetchone()
# if post_for_update == None:
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail=f"Post with the id {id} does not exist",
#     )
# update_post.update(
#     post.dict(),
#     synchronize_session=False,
# )
# db.commit()
# conn.commit()

# index = find_index_post(id)
# if index == None:
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail=f"Post with the ide {id} does not exist",
#     )
# post_dict = post.dict()
# post_dict["id"] = id
# post_dict["content"] = "New content"

# my_posts[index] = post_dict
# return {"data": "succcess!"}


# @app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     hashed_password = utils.hash(user.password)
#     user.password = hashed_password
#     new_user = models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


# @app.get("/users/{id}", response_model=schemas.UserOut)
# def get_user(id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User with id {id} does not exist.",
#         )
#     return user
