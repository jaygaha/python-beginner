from fastapi import FastAPI, HTTPException, Form, File, UploadFile
from models.model import ProductCreate, ProductUpdate, ProductResponse, UserProfile, ContactForm
from typing import List
from datetime import datetime

app = FastAPI()

# Mock database
products_db = []
next_product_id = 1

@app.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate):
    global next_product_id
    product_dict = product.model_dump()
    product_dict.update({
        "id": next_product_id,
        "created_at": datetime.now(),
        "updated_at": None
    })
    products_db.append(product_dict)
    next_product_id += 1
    return product_dict

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_update: ProductUpdate):
    product = next((p for p in products_db if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        product[field] = value
    product["updated_at"] = datetime.now()

    return product

@app.post("/products/batch/", response_model=List[ProductResponse])
def create_products_batch(products: List[ProductCreate]):
    global next_product_id
    created_products = []

    for product in products:
        product_dict = product.model_dump()
        product_dict.update({
            "id": next_product_id,
            "created_at": datetime.now(),
            "updated_at": None
        })
        products_db.append(product_dict)
        created_products.append(product_dict)
        next_product_id += 1

    return created_products

@app.post("/users/{user_id}/profile")
def update_user_profile(user_id: int, profile: UserProfile):
    # Simulate updating user profile
    return {
        "user_id": user_id,
        "profile": profile.model_dump(exclude_unset=True),
        "updated_at": datetime.now()
    }

# Form data endpoints
@app.post("/contact/")
def submit_contact_form(contact: ContactForm):
    # Simulate processing contact form
    return {
        "message": "Contact form submitted successfully",
        "reference_id": f"REF-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "data": contact.model_dump()
    }

@app.post("/products/form/")
def create_product_form(
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    category: str = Form(...),
    tags: str = Form("")  # Comma-separated tags
):
    # Parse tags
    tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()] if tags else []

    global next_product_id
    product_dict = {
        "id": next_product_id,
        "name": name,
        "description": description,
        "price": price,
        "category": category,
        "tags": tag_list,
        "created_at": datetime.now(),
        "updated_at": None
    }
    products_db.append(product_dict)
    next_product_id += 1
    return product_dict

@app.post("/upload/")
def upload_file(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file.size if hasattr(file, 'size') else 0
    }

@app.post("/upload/multiple/")
def upload_multiple_files(files: List[UploadFile] = File(...)):
    file_info = []
    for file in files:
        file_info.append({
            "filename": file.filename,
            "content_type": file.content_type,
            "size": file.size if hasattr(file, 'size') else 0
        })
    return {"files": file_info, "count": len(files)}

@app.post("/products/{product_id}/image/")
def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    alt_text: str = Form(None)
):
    product = next((p for p in products_db if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "product_id": product_id,
        "image": {
            "filename": file.filename,
            "content_type": file.content_type,
            "alt_text": alt_text
        }
    }

# Mixed parameters
@app.post("/products/{product_id}/review/")
def add_product_review(
    product_id: int,
    rating: int = Form(..., ge=1, le=5),
    title: str = Form(...),
    content: str = Form(...),
    images: List[UploadFile] = File(None),
    anonymous: bool = Form(False)
):
    product = next((p for p in products_db if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    review_data = {
        "product_id": product_id,
        "rating": rating,
        "title": title,
        "content": content,
        "anonymous": anonymous,
        "created_at": datetime.now()
    }

    if images:
        review_data["images"] = [
            {"filename": img.filename, "content_type": img.content_type}
            for img in images
        ]

    return review_data
