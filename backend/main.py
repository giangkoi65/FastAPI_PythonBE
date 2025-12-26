from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend.models import Product
from backend.database import SessionLocal, engine
import backend.database_models
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

backend.database_models.Base.metadata.create_all(bind=engine)

products = [
    Product(
        id=1, name="laptop", description="A powerful laptop", price=1200.0, amount=10
    ),
    Product(
        id=2,
        name="smartphone",
        description="A latest model smartphone",
        price=800.0,
        amount=25,
    ),
    Product(
        id=3,
        name="headphones",
        description="Noise-cancelling headphones",
        price=150.0,
        amount=50,
    ),
]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = SessionLocal()
    try:
        count = db.query(backend.database_models.Product).count()
        if count == 0:
            for product in products:
                db.add(backend.database_models.Product(**product.model_dump()))
            db.commit()
    finally:
        db.close()


init_db()


@app.get("/products/")
def get_all_products_db(db: Session = Depends(get_db)):
    db_products = db.query(backend.database_models.Product).all()
    return db_products


@app.get("/products/{product_id}")
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    db_product = (
        db.query(backend.database_models.Product)
        .filter(backend.database_models.Product.id == product_id)
        .first()
    )
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.post("/products/")
def add_product_db(product: Product, db: Session = Depends(get_db)):
    db_product = backend.database_models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.put("/products/{product_id}")
def update_product_db(product_id: int, updated_product: Product, db: Session = Depends(get_db)):
    db_product = (
        db.query(backend.database_models.Product)
        .filter(backend.database_models.Product.id == product_id)
        .first()
    )
    if db_product:
        db_product.name = updated_product.name
        db_product.description = updated_product.description
        db_product.price = updated_product.price
        db_product.amount = updated_product.amount
        db.commit()
        db.refresh(db_product)
        return db_product
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
def delete_product_db(product_id: int, db: Session = Depends(get_db)):
    db_product = (
        db.query(backend.database_models.Product)
        .filter(backend.database_models.Product.id == product_id)
        .first()
    )
    if db_product:
        db.delete(db_product)
        db.commit()
        return {"message": "Product deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Product not found")
    
@app.post("/add_product")
def add_product(product: Product):
    products.append(product)
    return {"message": "Product added successfully", "product": product}


@app.put("/update_product/{product_id}")
def update_product(product_id: int, updated_product: Product, db: Session = Depends(get_db)):
    for index, product in enumerate(products):
        if product["id"] == product_id:
            products[index] = updated_product
            return {
                "message": "Product updated successfully",
                "product": updated_product,
            }
    return {"message": "Product not found"}


@app.delete("/delete_product/{product_id}")
def delete_product(product_id: int):
    for i in range(len(products)):
        if products[i]["id"] == product_id:
            del products[i]
            return {"message": "Da xoa san pham"}
