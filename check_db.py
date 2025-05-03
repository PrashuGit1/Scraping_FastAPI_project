from app.database import SessionLocal
from app.models import Product

db = SessionLocal()
products = db.query(Product).all()

print(f"Total products found: {len(products)}")

for p in products:
    print(f"Name: {p.name}, Price: {p.price}, Discount: {p.discount}")
