from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import User
# from app.dependencies import get_current_user, get_db
from app.schemas import LoginRequest, SignupRequest, TokenResponse, UserResponse
from app.security import create_access_token, hash_password, verify_password


user_router = APIRouter(tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# @user_router.post("/auth/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
# def register(payload: SignupRequest, db: Session = Depends(get_db)):
#     existing = db.query(User).filter(User.email == payload.email).first()
#     if existing:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     user = User(
#         name=payload.name,
#         email=payload.email,
#         password_hash=hash_password(payload.password),
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     token = create_access_token(str(user.id))
#     return TokenResponse(access_token=token)


# @user_router.post("/auth/login", response_model=TokenResponse)
# def login(payload: LoginRequest, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == payload.email).first()
#     if not user or not verify_password(payload.password, user.password_hash):
#         raise HTTPException(status_code=401, detail="Incorrect email or password")

#     token = create_access_token(str(user.id))
#     return TokenResponse(access_token=token)


@user_router.get("/users/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user
