from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, database, auth
from app.models import User

router = APIRouter(prefix="/orders", tags=["Orders"])

# ------------------- GET ALL ORDERS --------------------
@router.get("/", response_model=list[schemas.OrderOut])
def read_orders(db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    return crud.get_orders(db)

# ------------------- CREATE ORDER --------------------
@router.post("/", response_model=schemas.OrderOut)
def create_order(order: schemas.OrderCreate, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    order.user_id = current_user.id
    return crud.create_order(db, order)

# ------------------- UPDATE ORDER STATUS --------------------
@router.put("/{order_id}", response_model=schemas.OrderOut)
def update_order_status(order_id: int, status: str, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    updated_order = crud.update_order_status(db, order_id, status)
    if not updated_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return updated_order

# ------------------- DELETE ORDER --------------------
@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    deleted = crud.delete_order(db, order_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return {"message": "Order deleted successfully"}
