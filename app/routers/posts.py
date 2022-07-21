from typing import Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter

from ..oauth2 import get_current_user


from .. import models, schemas
from fastapi import Response, status, HTTPException, Depends

from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("")
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
    limit: int = 1,
    skip: int = 0,
    search: Optional[str] = "",
):
    # Query oldfashioned, raw SQL way.
    posts = (
        db.query(models.Post)
        .filter(models.Post.owner_id == current_user.id)
        .limit(limit)
        .offset(skip)
        .filter(models.Post.content.contains(search))
        .all()
    )
    return posts


# Be careful, bellow route matches also "/posts/details/..." or similar. Solution: order of routes is important.
@router.get("/posts/{id}")
def get_post(
    id: int,
    response: Response,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
    limit: int = 1,
):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    # cursor.execute("""SELECT * FROM post WHERE id = %s""" % (str(id)))
    # post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Requested post not found"
        )
    return {"data": post}


@router.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):

    # new_post = models.Post(
    #     title=post.title, content=post.content, published=post.published
    # )

    # The following is the same as the lines above:
    print("user_id: ", user_id.id)
    new_post = models.Post(owner_id=user_id.id, **post.dict())
    print("New post: ", new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
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
    if new_post.owner_id != user_id.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform the requested action.",
        )
    print("All OK")
    print(vars(new_post))
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""" % (str(id)))
    # deleted_post = cursor.fetchone()
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with the id of {id} does not exist",
        )
    else:
        # import pdb

        # pdb.set_trace()
        if post.owner_id != user_id.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to perform the requested action.",
            )
        post_query.delete(synchronize_session=False)
        db.commit()
    # conn.commit()
    # index = find_index_post(id)
    # if index == None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Post with the ide {id} does not exist",
    #     )
    # my_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    update_post = db.query(models.Post).filter(models.Post.id == id)
    post_for_update = update_post.first()
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
    if post_for_update == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with the id {id} does not exist",
        )

    if post_for_update.owner_id != user_id.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform the requested action.",
        )
    update_post.update(
        post.dict(),
        synchronize_session=False,
    )
    db.commit()
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
    return {"data": "succcess!"}
