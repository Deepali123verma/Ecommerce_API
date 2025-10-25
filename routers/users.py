from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app import crud, schemas, database, utils, models, auth

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# -------------------- CREATE USER --------------------
@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Check if email already exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password safely (bcrypt max 72 bytes)
    hashed_password = utils.hash_password(user.password[:72])

    # Create new user
    new_user = models.User(name=user.name, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# -------------------- GET ALL USERS --------------------
@router.get("/", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(database.get_db)):
    return crud.get_users(db)


# -------------------- GET USER BY ID --------------------
@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# -------------------- DELETE USER --------------------
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user_id)
    return {"message": "User deleted successfully"}


# -------------------- LOGIN / TOKEN --------------------
@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    #  Find user by email (OAuth2 uses username field)
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    #  Verify password
    if not utils.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    #  Create token
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

    # Return token
    return {"access_token": access_token, "token_type": "bearer"}
