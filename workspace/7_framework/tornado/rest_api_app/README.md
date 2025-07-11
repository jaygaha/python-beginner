# Tornado REST API Application

A simple REST API built with Python's Tornado web framework that provides CRUD operations for managing items.

## Features

- **GET /items** - Retrieve all items
- **POST /items** - Create a new item
- **GET /items/{id}** - Retrieve a specific item by ID
- **PUT /items/{id}** - Update an existing item
- **DELETE /items/{id}** - Delete an item

## Requirements

- Python 3.7+
- Tornado web framework

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install Tornado directly:
```bash
pip install tornado
```

2. (Optional) Install coverage for test coverage reports:
```bash
pip install coverage
```

2. Clone or download the application files

## Usage

### Starting the Server

Run the application:
```bash
python app.py
```

The server will start on `http://localhost:8880`

### API Endpoints

#### 1. Get All Items
```
GET /items
```

**Response:**
```json
[
  {"id": 1, "name": "Item 1"},
  {"id": 2, "name": "Item 2"},
  {"id": 3, "name": "Item 3"}
]
```

#### 2. Create New Item
```
POST /items
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "New Item"
}
```

**Response (201 Created):**
```json
{
  "id": 4,
  "name": "New Item"
}
```

#### 3. Get Item by ID
```
GET /items/{id}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Item 1"
}
```

**Response (404 Not Found):**
```json
{
  "error": "Item not found"
}
```

#### 4. Update Item
```
PUT /items/{id}
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Updated Item Name"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Updated Item Name"
}
```

#### 5. Delete Item
```
DELETE /items/{id}
```

**Response:** 204 No Content

## Testing with cURL

### Get all items:
```bash
curl http://localhost:8880/items
```

### Create a new item:
```bash
curl -X POST http://localhost:8880/items \
  -H "Content-Type: application/json" \
  -d '{"name": "My New Item"}'
```

### Get a specific item:
```bash
curl http://localhost:8880/items/1
```

### Update an item:
```bash
curl -X PUT http://localhost:8880/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Item"}'
```

### Delete an item:
```bash
curl -X DELETE http://localhost:8880/items/1
```

## Data Storage

This application uses in-memory storage for simplicity. Data will be lost when the server restarts. For production use, consider integrating with a database like:

- PostgreSQL
- MySQL
- MongoDB
- SQLite

## Code Structure

- `ItemListHandler` - Handles `/items` endpoint (GET, POST)
- `ItemHandler` - Handles `/items/{id}` endpoint (GET, PUT, DELETE)
- `make_app()` - Creates and configures the Tornado application
- `items` - In-memory list storing the item data

## Error Handling

The API includes basic error handling:
- 400 Bad Request for malformed JSON
- 404 Not Found for non-existent items
- 201 Created for successful item creation
- 204 No Content for successful deletion

## Development Notes

- Server runs on port 8880 by default
- All responses are in JSON format
- CORS headers are not configured (add if needed for browser requests)
- No authentication/authorization implemented
- Input validation is minimal

## Testing

### Running Tests

The application includes comprehensive unit tests using Tornado's testing framework.

To run the tests:

```bash
python test_app.py
```

Or using unittest:

```bash
python -m unittest test_app.py
```

For verbose output:

```bash
python -m unittest test_app.py -v
```

### Test Runner Script

For convenience, use the provided test runner script:

```bash
# Run tests with normal verbosity
python run_tests.py

# Run tests with verbose output  
python run_tests.py verbose

# Run tests with minimal output
python run_tests.py quiet

# Run tests with coverage report (requires: pip install coverage)
python run_tests.py coverage

# Show help
python run_tests.py help
```

### Test Coverage

The test suite covers:

#### Basic CRUD Operations
- **GET /items** - Retrieve all items (empty and populated lists)
- **POST /items** - Create new items (success, validation errors)
- **GET /items/{id}** - Get specific items (found and not found)
- **PUT /items/{id}** - Update items (success and not found)
- **DELETE /items/{id}** - Delete items (success and not found)

#### Error Handling
- Invalid JSON in request bodies
- Missing required fields
- Non-existent item IDs
- Invalid HTTP methods
- Malformed URLs

#### Integration Tests
- Complete CRUD workflow (create → read → update → delete)
- Data persistence verification
- State management between operations

#### HTTP Compliance
- Correct status codes (200, 201, 204, 400, 404, 405, 500)
- Content-Type headers
- Response body formats

### Test Structure

```python
class TestRestApi(tornado.testing.AsyncHTTPTestCase):
    def setUp(self):
        # Reset test data before each test
        
    def test_operation_success(self):
        # Test successful operations
        
    def test_operation_failure(self):
        # Test error conditions
        
    def test_integration_workflow(self):
        # Test complete workflows
```

### Key Test Features

- **Isolated Tests**: Each test resets the data to ensure independence
- **Comprehensive Coverage**: Tests both success and failure scenarios
- **Integration Testing**: Verifies complete workflows work end-to-end
- **HTTP Compliance**: Ensures proper status codes and headers
- **Error Handling**: Tests malformed requests and edge cases

### Sample Test Output

```
test_delete_all_items (__main__.TestRestApi) ... ok
test_delete_item_not_found (__main__.TestRestApi) ... ok
test_delete_item_success (__main__.TestRestApi) ... ok
test_get_item_not_found (__main__.TestRestApi) ... ok
test_get_item_success (__main__.TestRestApi) ... ok
test_get_items_empty_list (__main__.TestRestApi) ... ok
test_get_items_success (__main__.TestRestApi) ... ok
test_integration_workflow (__main__.TestRestApi) ... ok
test_post_item_success (__main__.TestRestApi) ... ok
test_put_item_success (__main__.TestRestApi) ... ok

----------------------------------------------------------------------
Ran 10 tests in 0.123s

OK
```

## Future Enhancements

- Add database integration
- Implement authentication and authorization
- Add input validation and sanitization
- Add logging
- Add CORS support
- Add API documentation (OpenAPI/Swagger)
- Add pagination for large datasets
- Add test coverage reporting
- Add performance testing
- Add API rate limiting
- Add continuous integration (CI/CD)
- Add Docker containerization
- Add configuration management