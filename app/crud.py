from sqlalchemy.orm import Session
from app import models, schemas
from app.utils import hash_password, encrypt_data, decrypt_data

def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.email = decrypt_data(user.email)
    return user

def get_user_by_email(db: Session, email: str):
    encrypted_email = encrypt_data(email)
    user = db.query(models.User).filter(models.User.email == encrypted_email).first()
    if user:
        user.email = decrypt_data(user.email)
    return user

def get_users(db: Session):
    users = db.query(models.User).all()
    for user in users:
        user.email = decrypt_data(user.email)
    return users

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=encrypt_data(user.email),
        password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_user.email = decrypt_data(db_user.email)
    return db_user

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
