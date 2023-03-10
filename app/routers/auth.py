from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, models, oauth2, schemas, utils

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(
    # credentials: OAuth2PasswordRequestForm = Depends(),
    credentials: schemas.UserLogin,
    db: Session = Depends(database.get_db),
) -> schemas.Token:
    """Login user"""

    user = db.query(models.User).filter(models.User.email == credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invaild credentials."
        )

    if not utils.verify(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials."
        )

    access_token = oauth2.create_access_token({"user_id": user.id})

    return {"access_token": access_token, "token_type": "Bearer"}
