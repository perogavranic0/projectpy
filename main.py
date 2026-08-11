from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session, engine
import database_models 
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)
database_models.Base.metadata.create_all(bind = engine)

products = [
    Product(id=1,name="Phone",description="Iphone", price=41,quantity=12),
    Product(id=2,name="Laptop",description="Gaming laptop", price=3341,quantity=10)
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = session()
    count = db.query(database_models.Product).count

    if count == 0:

        for product in products:
            db.add(database_models.Product(**product.model_dump()))

    db.commit()

init_db()

@app.get("/")
def index():
    return "Hello"

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/products/{id}")

def get_product_id(id: int,db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()

    if db_product:
        return db_product

    return "Product not found"

@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product


@app.put("/products/{id}")
def update_product(id: int,product:Product,db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:

        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity

        db.commit()
        return "Product updated"

    else:
        return "No product found"


@app.delete("/products/{id}")
def delete_prduct(id: int,db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()    
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted"

    else:    
        return "No product found"