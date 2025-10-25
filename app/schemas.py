from pydantic import BaseModel
from typing import List, Optional

# ------------------- USERS -------------------
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    model_config = {
        "from_attributes": True  # Pydantic V2 replacement for orm_mode
    }

# ------------------- PRODUCTS -------------------
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    model_config = {
        "from_attributes": True
    }

# ------------------- ORDER ITEMS -------------------
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

# Include order_id for creating a new order item
class OrderItemCreate(OrderItemBase):
    order_id: int

class OrderItemOut(OrderItemBase):
    id: int
    order_id: int
    model_config = {
        "from_attributes": True
    }

# ------------------- ORDERS -------------------
class OrderBase(BaseModel):
    user_id: int
    total_amount: float
    status: Optional[str] = "pending"

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderOut(OrderBase):
    id: int
    items: List[OrderItemOut] = []
    model_config = {
        "from_attributes": True
    }
# ------------------- TOKEN -------------------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: int | None = None

