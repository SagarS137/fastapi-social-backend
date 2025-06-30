from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from app import utils, schemas, models
from app.database import get_db


router = APIRouter(prefix="/users", tags=["Users"])
# router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash_password(user.password)
    user_dict = user.model_dump()
    user_dict["password"] = hashed_password
    new_user = models.Users(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {user_id} not found")
    return user