"""
Test file to demonstrate the fixed functionality of the Todo API
"""
import requests
import json

BASE_URL = "http://localhost:8880"

def test_api():
    print("Testing Todo API...")

    # Test 1: Get all users
    print("\n1. Testing GET /users")
    response = requests.get(f"{BASE_URL}/users")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # Test 2: Get specific user
    print("\n2. Testing GET /user?id=1")
    response = requests.get(f"{BASE_URL}/user?id=1")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # Test 3: Get user with invalid ID
    print("\n3. Testing GET /user?id=invalid")
    response = requests.get(f"{BASE_URL}/user?id=invalid")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # Test 4: Get all todos
    print("\n4. Testing GET /todos")
    response = requests.get(f"{BASE_URL}/todos")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # Test 5: Get todos for specific user
    print("\n5. Testing GET /todos?user_id=1")
    response = requests.get(f"{BASE_URL}/todos?user_id=1")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # Test 6: Create new todo
    print("\n6. Testing POST /todo")
    new_todo = {
        "title": "Test Todo",
        "description": "This is a test todo",
        "user_id": 1
    }
    response = requests.post(f"{BASE_URL}/todo", json=new_todo)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # Test 7: Create todo with invalid data
    print("\n7. Testing POST /todo with invalid data")
    invalid_todo = {
        "title": "",
        "description": "Missing title",
        "user_id": "invalid"
    }
    response = requests.post(f"{BASE_URL}/todo", json=invalid_todo)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # Test 8: Get specific todo
    print("\n8. Testing GET /todos/1")
    response = requests.get(f"{BASE_URL}/todos/1")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # Test 9: Update todo
    print("\n9. Testing PUT /todo?id=1")
    updated_todo = {
        "title": "Updated Todo",
        "description": "This todo has been updated",
        "completed": True
    }
    response = requests.put(f"{BASE_URL}/todo?id=1", json=updated_todo)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # Test 10: Toggle todo completion
    print("\n10. Testing PATCH /todo/2/toggle")
    response = requests.patch(f"{BASE_URL}/todo/2/toggle")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # Test 11: Delete todo
    print("\n11. Testing DELETE /todo?id=1")
    response = requests.delete(f"{BASE_URL}/todo?id=1")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # Test 12: Try to get deleted todo
    print("\n12. Testing GET /todos/1 (should be 404)")
    response = requests.get(f"{BASE_URL}/todos/1")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the server is running on http://localhost:8880")
        print("Run: python main.py")
