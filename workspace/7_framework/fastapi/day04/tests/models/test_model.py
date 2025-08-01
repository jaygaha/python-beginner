import pytest
from datetime import datetime
from src.models.model import (
    ProductBase, ProductCreate, ProductUpdate, ProductResponse,
    UserProfile, ContactForm
)

# ----------- ProductBase Tests -----------

def test_product_base_valid():
    product = ProductBase(
        name="Test Product",
        description="A useful product.",
        price=19.99,
        category="Tools",
        tags=["utility", "hardware"]
    )
    assert product.name == "Test Product"
    assert product.price == 19.99

@pytest.mark.parametrize("field,value", [
    ("name", ""),  # too short
    ("name", "a" * 101),  # too long
    ("description", "a" * 501),  # too long
    ("price", 0),  # must be > 0
])
def test_product_base_invalid(field, value):
    data = {
        "name": "Valid",
        "price": 10.0,
        "category": "General"
    }
    data[field] = value
    with pytest.raises(Exception):
        ProductBase(**data)

# ----------- ProductCreate Tests -----------

def test_product_create_inherits_base():
    product = ProductCreate(
        name="Created Product",
        price=9.99,
        category="Books"
    )
    assert isinstance(product, ProductBase)

# ----------- ProductUpdate Tests -----------

def test_product_update_partial():
    update = ProductUpdate(price=25.0)
    assert update.price == 25.0
    assert update.name is None

def test_product_update_invalid_price():
    with pytest.raises(Exception):
        ProductUpdate(price=0)

# ----------- ProductResponse Tests -----------

def test_product_response_valid():
    now = datetime.now()
    product = ProductResponse(
        id=1,
        name="Full Product",
        description="Detailed",
        price=49.99,
        category="Electronics",
        tags=["tech"],
        created_at=now
    )
    assert product.id == 1
    assert product.created_at == now

# ----------- UserProfile Tests -----------

def test_user_profile_optional_fields():
    profile = UserProfile()
    assert profile.bio is None
    assert profile.website is None

# ----------- ContactForm Tests -----------

def test_contact_form_valid():
    form = ContactForm(
        name="Jane Doe",
        email="jane.doe@example.com",
        subject="Question about product",
        message="Can you tell me more about this item?",
        urgent=True
    )
    assert form.urgent is True

@pytest.mark.parametrize("email", [
    "invalid-email",
    "missing@domain",
    "@nouser.com",
    "user@.com"
])
def test_contact_form_invalid_email(email):
    with pytest.raises(Exception):
        ContactForm(
            name="Jane",
            email=email,
            subject="Hello World",
            message="This is a valid message content."
        )

@pytest.mark.parametrize("field,value", [
    ("name", "A"),  # too short
    ("subject", "Hey"),  # too short
    ("message", "Short msg"),  # too short
])
def test_contact_form_invalid_fields(field, value):
    data = {
        "name": "John",
        "email": "john@example.com",
        "subject": "Hello there",
        "message": "This message is valid and long enough."
    }
    data[field] = value
    with pytest.raises(Exception):
        ContactForm(**data)
