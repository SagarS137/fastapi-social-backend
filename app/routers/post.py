from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import func
from app import models, schemas, Oauth2
from app.database import get_db


router = APIRouter(prefix="/posts", tags=["Posts"])

# @app.get("/posts")  # Get all posts
# def get_posts():
#     cursor.execute("SELECT * FROM posts")
#     posts = cursor.fetchall()
#     return {"data": posts}


# Get all posts with SQLAlchemy
@router.get("/", response_model=list[schemas.Postvote])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user),
              limit: int = 5, skip: int = 0, search: Optional[str] = ""):
    print(current_user.email)
    all_posts = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")
                       ).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(
                           models.Post.id).order_by(models.Post.id.asc()
                            ).filter(models.Post.title.contains(search)
                            ).limit(limit).offset(skip).all()
    if not all_posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")

    return [schemas.Postvote(post=post, votes=votes) for post, votes in all_posts]


# @app.post("/posts", status_code=status.HTTP_201_CREATED)  # Create a new post
# def create_posts(post: Post):
#     cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
#                    (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"message": "Post created successfully", "new_post": new_post}


# Create a new post with SQLAlchemy
@router.post("/", status_code=status.HTTP_201_CREATED,  response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(Oauth2.get_current_user)):
    
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # used model dump to convert Pydantic model to SQLAlchemy model,
    # no need to manually assign each field like above

    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# @app.get("/posts/{post_id}")  # Get a post by its ID
# def get_post(post_id: int):
#     cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
#     post = cursor.fetchone()
#     if post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with id {post_id} not found")
#     return {"post_detail": post}


# Get a post by its ID with SQLAlchemy
@router.get("/{post_id}",  response_model=schemas.Postvote)
def get_post(post_id: int, db: Session = Depends(get_db),current_user: int = Depends(Oauth2.get_current_user)):
    
    spcecific_post = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")
                       ).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(
                           models.Post.id).filter(models.Post.id == post_id).first()
    print(current_user.email)

    if spcecific_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {post_id} not found")
    
    post, votes = spcecific_post

    return schemas.Postvote(post=post, votes=votes)

# Delete a post by its ID
# @app.delete("/posts/{post_id}", status_code=status.HTTP_202_ACCEPTED)
# def delete_post(post_id: int):
#     cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (post_id,))
#     post = cursor.fetchone()
#     conn.commit()
#     if post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with id {post_id} not found")
#     return {"message": "Post deleted successfully"}


# Delete a post by its ID with SQLAlchemy
@router.delete("/{post_id}", status_code=status.HTTP_202_ACCEPTED)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    
    # post = db.query(models.Post).filter(models.Post.id == post_id).delete(synchronize_session=False) 
    # above query deletes w/o checking if its same user's post

    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {post_id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to delete this post")

    post_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Post deleted successfully"}


# Update a post by its ID
# @app.put("/posts/{post_id}")
# def update_post(post_id: int, post: Post):
#     cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
#                    (post.title, post.content, post.published, post_id))
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if updated_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with id {post_id} not found")
#     return {"message": "Post updated successfully", "post": post}


# Update a post by its ID with SQLAlchemy
@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(Oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    updated_query = post_query.first()

    if updated_query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {post_id} not found")

    if updated_query.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to delete this post")

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return updated_query
