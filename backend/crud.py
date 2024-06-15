from sqlalchemy.orm import Session
from . import models, schemas

def get_product_by_code(db: Session, code: str):
    return db.query(models.Product).filter(models.Product.code == code).first()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(
        emp_code=transaction.emp_code,
        store_code=transaction.store_code,
        pos_no=transaction.pos_no,
        total_amt=0  # 初期値は0
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    total_amt = 0

    for detail in transaction.details:
        db_detail = models.TransactionDetail(
            transaction_id=db_transaction.id,
            product_code=detail.product_code,
            product_name=detail.product_name,
            product_price=detail.product_price
        )
        db.add(db_detail)
        db.commit()
        db.refresh(db_detail)
        total_amt += db_detail.product_price

    db_transaction.total_amt = total_amt
    db.commit()
    db.refresh(db_transaction)
    return db_transaction