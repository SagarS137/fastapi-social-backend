from typing import Literal
from datetime import datetime
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):  # Pydantic model for post validation
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):  # Pydantic model for creating a post
    pass

class UserOut(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner: UserOut
    
    class Config:
        from_attributes = True # Pydantic model to convert SQLAlchemy model attributes to Pydantic model

class Postvote(BaseModel):
    post: PostResponse
    votes: int

    class Config:
        from_attributes = True 






class UserCreate(BaseModel):  # Pydantic model for user validation
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True  





class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None  # Optional user ID, can be None if not authenticated

    



class Vote(BaseModel):
    post_id: int
    dir: Literal[0,1]
    