from fastapi import FastAPI
from models import Product

app = FastAPI()

products = [
    {
        "id": 1,
        "name": "Laptop",
        "description": "A personal computer for mobile use.",
        "price": 1000,
        "amount": 5,
    },
    {
        "id": 2,
        "name": "Smartphone",
        "description": "A handheld personal computer.",
        "price": 700,
        "amount": 10,
    },
    {
        "id": 3,
        "name": "Tablet",
        "description": "A portable touch-screen computer.",
        "price": 500,
        "amount": 7,
    },
]


@app.get("/products")
def get_all_products():
    #db connection
    #query
    return products


@app.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    return {"message": "Product not found"}


@app.post("/add_product")
def add_product(product: Product):
    products.append(product)
    return {"message": "Product added successfully", "product": product}


@app.put("/update_product/{product_id}")
def update_product(product_id: int, updated_product: Product):
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
            return{"message": "Da xoa san pham"}
        
