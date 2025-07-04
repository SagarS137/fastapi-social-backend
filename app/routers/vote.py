from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from app import schemas, models, Oauth2, database


router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote_data: schemas.Vote, db: Session = Depends(database.get_db), current_user: models.Users = Depends(Oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote_data.post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote_data.post_id} does not exist")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote_data.post_id, models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()
    
    if vote_data.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"User {current_user.id} has already voted on post {vote_data.post_id}")
        
        new_vote = models.Vote(post_id=vote_data.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote removed successfully"}
