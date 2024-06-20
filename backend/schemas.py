from pydantic import BaseModel
from datetime import datetime
from typing import List

class ProductBase(BaseModel):
    code: str
    name: str
    price: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

class TransactionDetailBase(BaseModel):
    product_code: str
    product_name: str
    product_price: int
    quantity: int

class TransactionDetailCreate(TransactionDetailBase):
    pass

class TransactionDetail(TransactionDetailBase):
    id: int

    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    datetime: datetime
    emp_code: str
    store_code: str
    pos_no: str
    total_amt: int

class TransactionCreate(TransactionBase):
    details: List[TransactionDetailCreate]

class Transaction(TransactionBase):
    id: int
    details: List[TransactionDetail] = []

    class Config:
        orm_mode = True
