from sqlalchemy.orm import Session
from app import models, schemas

# Get all products
def get_products(db: Session):
    return db.query(models.Product).all()

# Get a single product by ID
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

# Create a new product
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        name=product.name,
        price=product.price,
        discount=product.discount
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Delete a product
def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return True
    return False

