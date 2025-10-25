from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, models, schemas, database, auth
from app.models import User

router = APIRouter(prefix="/order-items", tags=["Order Items"])

# ------------------- GET ALL ORDER ITEMS --------------------
@router.get("/", response_model=list[schemas.OrderItemOut])
def read_order_items(db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    return db.query(models.OrderItem).all()

# ------------------- CREATE ORDER ITEM --------------------
@router.post("/", response_model=schemas.OrderItemOut)
def create_order_item(order_item: schemas.OrderItemCreate, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    order = db.query(models.Order).filter(models.Order.id == order_item.order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to add items to this order")

    db_item = models.OrderItem(**order_item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# ------------------- UPDATE ORDER ITEM --------------------
@router.put("/{item_id}", response_model=schemas.OrderItemOut)
def update_order_item(item_id: int, order_item: schemas.OrderItemCreate, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    db_item = db.query(models.OrderItem).filter(models.OrderItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order item not found")
    order = db_item.order
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to update this order item")

    for key, value in order_item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

# ------------------- DELETE ORDER ITEM --------------------
@router.delete("/{item_id}")
def delete_order_item(item_id: int, db: Session = Depends(database.get_db), current_user: User = Depends(auth.get_current_user)):
    db_item = db.query(models.OrderItem).filter(models.OrderItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order item not found")
    order = db_item.order
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this order item")

    db.delete(db_item)
    db.commit()
    return {"message": "Order item deleted successfully"}
