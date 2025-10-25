from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, database, auth
from app.models import User

router = APIRouter(prefix="/products", tags=["Products"])

# ------------------- GET ALL PRODUCTS --------------------
@router.get("/", response_model=list[schemas.ProductOut])
def read_products(db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    """
    Get all products (protected route, requires token)
    """
    return crud.get_products(db)

# ------------------- CREATE PRODUCT --------------------
@router.post("/", response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    """
    Create a new product (protected route)
    """
    return crud.create_product(db, product)

# ------------------- UPDATE PRODUCT --------------------
@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: int, product_data: schemas.ProductCreate, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    updated_product = crud.update_product(db, product_id, product_data.dict())
    if not updated_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return updated_product

# ------------------- DELETE PRODUCT --------------------
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    deleted = crud.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return {"message": "Product deleted successfully"}
