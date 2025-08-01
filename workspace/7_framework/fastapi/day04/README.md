# FastAPI Day 04: Request Body and Form Data

Welcome to **Day 04** of the FastAPI tutorial! Today you'll learn how to handle JSON request bodies, work with form data and file uploads, and combine different types of parameters in your API endpoints.

---

## What You'll Learn

- How to handle and validate JSON request bodies
- How to work with form data and file uploads
- How to manage different content types in FastAPI
- How to combine path, query, and body parameters in endpoints
- How to write automated tests for these features

---

## Key Concepts

### 1. Request Body

- **Request bodies** are used to send structured data (usually JSON) to your API.
- FastAPI uses Pydantic models to validate and parse incoming request bodies.

Example request body:
```
POST /products/
{
  "name": "New Product",
  "description": "A great item",
  "price": 19.99,
  "category": "tools",
  "tags": ["utility", "hardware"]
}
```

### 2. Form Data

- **Form data** is commonly used for HTML forms and file uploads.
- FastAPI provides the `Form` and `File` classes to handle form fields and file uploads.

Example form data:
```
POST /products/form/
name=Form Product
description=Created via form
price=15.99
category=tools
tags=form,test,product
```

### 3. File Uploads

- Use `UploadFile` to receive files in your endpoints.
- FastAPI supports single and multiple file uploads.

Example file upload:
```
POST /upload/
[file: test.txt]
```

### 4. Combining Parameters

- FastAPI allows you to combine path, query, body, and form parameters in a single endpoint.
- This is useful for complex operations like submitting reviews with images or updating resources with additional metadata.

Example mixed parameters:
```
POST /products/{product_id}/review/
Form fields: rating, title, content, anonymous
Files: images[]
```

---

## Next Steps

- Try sending requests to your API with JSON bodies, form data, and file uploads.
- Explore the code to see how validation and parsing are implemented for each type.
- Run the tests to ensure everything works as expected!

---

**Tip:** FastAPI’s automatic docs are available at `/docs` when you run your app.

---
