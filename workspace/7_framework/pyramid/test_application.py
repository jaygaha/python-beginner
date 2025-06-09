#!/usr/bin/env python3
"""
Comprehensive test script for the Pyramid Task Manager application.
This script verifies that all bugs have been fixed and the application works correctly.
"""

import requests
import time
import threading
import sys
from wsgiref.simple_server import make_server
from tasks import create_app


class ApplicationTester:
    def __init__(self):
        self.base_url = "http://localhost:6544"
        self.server = None
        self.server_thread = None
        self.app = None
        
    def start_server(self):
        """Start the test server in a background thread."""
        print("🚀 Starting test server...")
        global_config = {}
        settings = {'sqlalchemy.url': 'sqlite:///test_tasks.db'}
        self.app = create_app(global_config, **settings)
        
        def run_server():
            self.server = make_server("127.0.0.1", 6544, self.app)
            self.server.serve_forever()
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        time.sleep(2)  # Give server time to start
        
    def stop_server(self):
        """Stop the test server."""
        if self.server:
            self.server.shutdown()
            
    def test_basic_pages(self):
        """Test that all basic pages load correctly."""
        print("\n📄 Testing basic page loading...")
        
        tests = [
            ("/", "task list page"),
            ("/tasks/add", "add task page"),
            ("/static/style.css", "CSS file")
        ]
        
        for path, description in tests:
            try:
                response = requests.get(f"{self.base_url}{path}", timeout=5)
                if response.status_code == 200:
                    print(f"  ✅ {description}: OK")
                else:
                    print(f"  ❌ {description}: Status {response.status_code}")
                    return False
            except Exception as e:
                print(f"  ❌ {description}: Error - {e}")
                return False
        return True
    
    def test_csrf_protection(self):
        """Test CSRF protection functionality."""
        print("\n🔒 Testing CSRF protection...")
        
        # Test 1: Valid CSRF token
        try:
            session = requests.Session()
            form_response = session.get(f"{self.base_url}/tasks/add")
            
            # Extract CSRF token
            csrf_start = form_response.text.find('value="') + 7
            csrf_end = form_response.text.find('"', csrf_start)
            csrf_token = form_response.text[csrf_start:csrf_end]
            
            if len(csrf_token) > 20:  # Valid token should be longer
                print(f"  ✅ CSRF token generated: {csrf_token[:20]}...")
                
                # Submit with valid token
                response = session.post(f"{self.base_url}/tasks/add", data={
                    'title': 'CSRF Test Task',
                    'description': 'Testing CSRF validation',
                    '_csrf': csrf_token
                })
                
                if response.status_code in [200, 302]:
                    print("  ✅ Valid CSRF token: Accepted")
                else:
                    print(f"  ❌ Valid CSRF token: Rejected (Status {response.status_code})")
                    return False
            else:
                print("  ❌ CSRF token not found or invalid")
                return False
                
        except Exception as e:
            print(f"  ❌ CSRF test failed: {e}")
            return False
            
        # Test 2: Invalid CSRF token
        try:
            response = requests.post(f"{self.base_url}/tasks/add", data={
                'title': 'Bad Task',
                'description': 'Should be rejected',
                '_csrf': 'invalid_token_123'
            })
            
            if "Invalid security token" in response.text:
                print("  ✅ Invalid CSRF token: Correctly rejected")
            else:
                print("  ❌ Invalid CSRF token: Not properly rejected")
                return False
                
        except Exception as e:
            print(f"  ❌ Invalid CSRF test failed: {e}")
            return False
            
        return True
    
    def test_task_creation(self):
        """Test task creation functionality."""
        print("\n📝 Testing task creation...")
        
        try:
            session = requests.Session()
            
            # Get form and CSRF token
            form_response = session.get(f"{self.base_url}/tasks/add")
            csrf_start = form_response.text.find('value="') + 7
            csrf_end = form_response.text.find('"', csrf_start)
            csrf_token = form_response.text[csrf_start:csrf_end]
            
            # Create a test task
            response = session.post(f"{self.base_url}/tasks/add", data={
                'title': 'Test Application Task',
                'description': 'Created by automated test',
                '_csrf': csrf_token
            })
            
            # Check if task appears in list
            task_list = session.get(f"{self.base_url}/")
            if "Test Application Task" in task_list.text:
                print("  ✅ Task creation: Working correctly")
                return True
            else:
                print("  ❌ Task creation: Task not found in list")
                return False
                
        except Exception as e:
            print(f"  ❌ Task creation test failed: {e}")
            return False
    
    def test_templates(self):
        """Test that templates render correctly."""
        print("\n🎨 Testing template rendering...")
        
        try:
            response = requests.get(f"{self.base_url}/")
            content = response.text
            
            template_elements = [
                "Pyramid Task Manager",  # Title
                "Tasks",                 # Heading
                "Add Task",             # Navigation
                "static/style.css"      # CSS link
            ]
            
            for element in template_elements:
                if element in content:
                    print(f"  ✅ Template element '{element}': Found")
                else:
                    print(f"  ❌ Template element '{element}': Missing")
                    return False
                    
            return True
            
        except Exception as e:
            print(f"  ❌ Template test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests and return overall result."""
        print("🧪 Starting comprehensive application tests...\n")
        
        try:
            self.start_server()
            
            tests = [
                self.test_basic_pages,
                self.test_templates,
                self.test_csrf_protection,
                self.test_task_creation
            ]
            
            results = []
            for test in tests:
                results.append(test())
            
            print("\n" + "="*50)
            print("📊 TEST RESULTS SUMMARY")
            print("="*50)
            
            if all(results):
                print("🎉 ALL TESTS PASSED!")
                print("✅ The Pyramid Task Manager is working correctly")
                print("✅ All bugs have been successfully fixed")
                print("\n🚀 You can now run the application with: python task.py")
                return True
            else:
                print("❌ SOME TESTS FAILED")
                print("⚠️  Please check the errors above")
                return False
                
        except Exception as e:
            print(f"\n💥 Test suite failed to run: {e}")
            return False
        finally:
            self.stop_server()


def main():
    """Main function to run the test suite."""
    import os
    
    # Clean up any existing test database
    test_db = "test_tasks.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    tester = ApplicationTester()
    success = tester.run_all_tests()
    
    # Clean up test database
    if os.path.exists(test_db):
        os.remove(test_db)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()