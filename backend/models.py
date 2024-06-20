from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(13), unique=True, index=True)
    name = Column(String(50))
    price = Column(Integer)

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime)
    emp_code = Column(String(10))
    store_code = Column(String(10))
    pos_no = Column(String(10))
    total_amt = Column(Integer)
    details = relationship("TransactionDetail", back_populates="transaction")

class TransactionDetail(Base):
    __tablename__ = "transaction_details"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    product_code = Column(String(13))
    product_name = Column(String(50))
    product_price = Column(Integer)
    quantity = Column(Integer)

    transaction = relationship("Transaction", back_populates="details")
    product = relationship("Product")
