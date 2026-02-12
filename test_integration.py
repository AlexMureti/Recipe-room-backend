#!/usr/bin/env python3
"""
Integration Test Script
Tests backend API endpoints and verifies they work correctly
Run this before deployment to ensure backend is working properly
"""

import requests
import sys
import json
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000"
API_BASE = f"{BACKEND_URL}/api"

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name):
    """Print test name"""
    print(f"\n{Colors.BLUE}Testing: {name}{Colors.END}")

def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def test_backend_running():
    """Test if backend is running"""
    print_test("Backend Server")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print_success(f"Backend is running on {BACKEND_URL}")
            return True
        else:
            print_error(f"Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error(f"Cannot connect to backend at {BACKEND_URL}")
        print_warning("Make sure backend is running: python app.py")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_api_root():
    """Test API root endpoint"""
    print_test("API Root Endpoint")
    try:
        response = requests.get(BACKEND_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success("API root endpoint accessible")
            print(f"  API Name: {data.get('name')}")
            print(f"  Version: {data.get('version')}")
            return True
        else:
            print_error(f"API root returned: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_cors_headers():
    """Test CORS headers"""
    print_test("CORS Configuration")
    try:
        headers = {
            'Origin': 'http://localhost:5173',
            'Access-Control-Request-Method': 'GET'
        }
        response = requests.options(f"{API_BASE}/auth/profile", headers=headers, timeout=5)
        
        cors_origin = response.headers.get('Access-Control-Allow-Origin')
        cors_methods = response.headers.get('Access-Control-Allow-Methods')
        
        if cors_origin:
            print_success(f"CORS enabled - Origin: {cors_origin}")
            if cors_methods:
                print(f"  Allowed methods: {cors_methods}")
            return True
        else:
            print_warning("CORS headers not found - might cause frontend issues")
            return True  # Don't fail, just warn
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_user_registration():
    """Test user registration"""
    print_test("User Registration")
    
    # Generate unique username
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    test_user = {
        "username": f"testuser_{timestamp}",
        "email": f"test_{timestamp}@example.com",
        "password": "TestPassword123!"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/register",
            json=test_user,
            timeout=5
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            print_success("User registration successful")
            print(f"  Username: {test_user['username']}")
            return test_user
        elif response.status_code == 400:
            print_warning("Registration validation error (expected if endpoint requires more fields)")
            print(f"  Response: {response.json()}")
            return None
        else:
            print_error(f"Registration failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None

def test_user_login(user_data):
    """Test user login"""
    print_test("User Login")
    
    if not user_data:
        print_warning("Skipping login test (no user data)")
        return None
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/login",
            json={
                "username": user_data["username"],
                "password": user_data["password"]
            },
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('token') or data.get('access_token')
            if token:
                print_success("Login successful")
                print(f"  Token received: {token[:20]}...")
                return token
            else:
                print_warning("Login successful but no token in response")
                return None
        else:
            print_error(f"Login failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None

def test_protected_endpoint(token):
    """Test accessing protected endpoint"""
    print_test("Protected Endpoint (Profile)")
    
    if not token:
        print_warning("Skipping protected endpoint test (no token)")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_BASE}/auth/profile",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            print_success("Protected endpoint accessible with token")
            return True
        elif response.status_code == 401:
            print_error("Token authentication failed")
            return False
        else:
            print_warning(f"Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def main():
    """Run all integration tests"""
    print(f"\n{'='*60}")
    print(f"{Colors.BLUE}Recipe Room - Integration Test Suite{Colors.END}")
    print(f"{'='*60}")
    print(f"Testing backend at: {BACKEND_URL}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        'passed': 0,
        'failed': 0,
        'warnings': 0
    }
    
    # Run tests
    tests = [
        ('Backend Running', test_backend_running, []),
        ('API Root', test_api_root, []),
        ('CORS Headers', test_cors_headers, []),
    ]
    
    # Run basic tests first
    for test_name, test_func, args in tests:
        try:
            result = test_func(*args)
            if result:
                results['passed'] += 1
            else:
                results['failed'] += 1
                if test_name == 'Backend Running':
                    print_error("\nBackend is not running. Cannot continue tests.")
                    sys.exit(1)
        except Exception as e:
            print_error(f"Test crashed: {str(e)}")
            results['failed'] += 1
    
    # Test user registration and authentication flow
    user_data = test_user_registration()
    if user_data:
        results['passed'] += 1
        token = test_user_login(user_data)
        if token:
            results['passed'] += 1
            if test_protected_endpoint(token):
                results['passed'] += 1
            else:
                results['failed'] += 1
        else:
            results['failed'] += 1
            results['warnings'] += 1
    else:
        results['failed'] += 1
        results['warnings'] += 2  # Skip login and protected endpoint
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"{Colors.BLUE}Test Summary{Colors.END}")
    print(f"{'='*60}")
    print(f"{Colors.GREEN}Passed: {results['passed']}{Colors.END}")
    print(f"{Colors.RED}Failed: {results['failed']}{Colors.END}")
    if results['warnings'] > 0:
        print(f"{Colors.YELLOW}Warnings: {results['warnings']}{Colors.END}")
    
    # Exit with appropriate code
    if results['failed'] == 0:
        print(f"\n{Colors.GREEN}All tests passed! ✓{Colors.END}")
        print(f"{Colors.GREEN}Backend is ready for deployment{Colors.END}\n")
        sys.exit(0)
    else:
        print(f"\n{Colors.RED}Some tests failed ✗{Colors.END}")
        print(f"{Colors.YELLOW}Please fix the issues before deploying{Colors.END}\n")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrupted by user{Colors.END}")
        sys.exit(1)
