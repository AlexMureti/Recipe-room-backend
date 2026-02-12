"""
Diagnostic Test Script for Recipe Room API
Tests all critical endpoints to identify integration issues
"""

import requests
import json
from pprint import pprint

BASE_URL = "http://localhost:8000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name, status, message=""):
    color = Colors.GREEN if status else Colors.RED
    symbol = "✓" if status else "✗"
    print(f"{color}{symbol} {name}{Colors.END}")
    if message:
        print(f"  {message}")
    print()

def test_api_health():
    """Test if API is running"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("TESTING API HEALTH")
    print(f"{'='*60}{Colors.END}\n")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print_test("API Health Check", True, f"Response: {response.json()}")
            return True
        else:
            print_test("API Health Check", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("API Health Check", False, f"Error: {str(e)}")
        return False

def test_auth_flow():
    """Test authentication endpoints"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("TESTING AUTHENTICATION FLOW")
    print(f"{'='*60}{Colors.END}\n")
    
    # Test user registration
    test_user = {
        "username": f"testuser_{int(requests.get(f'{BASE_URL}/health').elapsed.total_seconds() * 1000)}",
        "email": f"test_{int(requests.get(f'{BASE_URL}/health').elapsed.total_seconds() * 1000)}@example.com",
        "password": "TestPassword123"
    }
    
    try:
        # Register
        response = requests.post(f"{BASE_URL}/api/auth/register", json=test_user, timeout=5)
        if response.status_code in [200, 201]:
            print_test("User Registration", True, f"User: {test_user['username']}")
        else:
            print_test("User Registration", False, 
                      f"Status: {response.status_code}, Response: {response.text}")
            return None
        
        # Login
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            user_id = data.get('user', {}).get('id')
            print_test("User Login", True, f"Token received, User ID: {user_id}")
            return {"token": token, "user_id": user_id, "email": test_user["email"]}
        else:
            print_test("User Login", False, 
                      f"Status: {response.status_code}, Response: {response.text}")
            return None
            
    except Exception as e:
        print_test("Authentication", False, f"Error: {str(e)}")
        return None

def test_recipe_creation(auth_data):
    """Test recipe creation"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("TESTING RECIPE CREATION")
    print(f"{'='*60}{Colors.END}\n")
    
    if not auth_data:
        print_test("Recipe Creation", False, "No authentication data available")
        return None
    
    headers = {"Authorization": f"Bearer {auth_data['token']}"}
    
    recipe_data = {
        "title": "Test Recipe - Diagnostic",
        "description": "This is a test recipe for diagnostic purposes",
        "country": "Kenya",
        "ingredients": [
            {"name": "Flour", "quantity": "2 cups"},
            {"name": "Sugar", "quantity": "1 cup"},
            {"name": "Eggs", "quantity": "3"}
        ],
        "procedure": [
            {"step": 1, "instruction": "Mix all ingredients together in a bowl"},
            {"step": 2, "instruction": "Bake at 180°C for 30 minutes"},
            {"step": 3, "instruction": "Let it cool and serve"}
        ],
        "people_served": 4,
        "prep_time": 15,
        "cook_time": 30
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/recipes/",
            json=recipe_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            recipe_id = data.get('recipe', {}).get('recipe_id')
            print_test("Recipe Creation", True, f"Recipe ID: {recipe_id}")
            return recipe_id
        else:
            print_test("Recipe Creation", False, 
                      f"Status: {response.status_code}\nResponse: {response.text}")
            return None
            
    except Exception as e:
        print_test("Recipe Creation", False, f"Error: {str(e)}")
        return None

def test_group_creation(auth_data):
    """Test group creation"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("TESTING GROUP CREATION")
    print(f"{'='*60}{Colors.END}\n")
    
    if not auth_data:
        print_test("Group Creation", False, "No authentication data available")
        return None
    
    headers = {"Authorization": f"Bearer {auth_data['token']}"}
    
    group_data = {
        "name": "Test Group - Diagnostic",
        "description": "This is a test group for diagnostic purposes",
        "max_members": 10
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/groups/",
            json=group_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            group_id = data.get('group', {}).get('group_id')
            print_test("Group Creation", True, f"Group ID: {group_id}")
            print(f"  Group data returned: {json.dumps(data.get('group', {}), indent=2)}")
            return group_id
        else:
            print_test("Group Creation", False, 
                      f"Status: {response.status_code}\nResponse: {response.text}")
            return None
            
    except Exception as e:
        print_test("Group Creation", False, f"Error: {str(e)}")
        return None

def test_add_member_to_group(auth_data, group_id):
    """Test adding a member to a group"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("TESTING ADD MEMBER TO GROUP")
    print(f"{'='*60}{Colors.END}\n")
    
    if not auth_data or not group_id:
        print_test("Add Member", False, "Missing auth data or group ID")
        return False
    
    headers = {"Authorization": f"Bearer {auth_data['token']}"}
    
    # First, create a second user to invite
    test_user_2 = {
        "username": f"testuser2_{int(requests.get(f'{BASE_URL}/health').elapsed.total_seconds() * 1000)}",
        "email": f"test2_{int(requests.get(f'{BASE_URL}/health').elapsed.total_seconds() * 1000)}@example.com",
        "password": "TestPassword123"
    }
    
    try:
        # Register second user
        response = requests.post(f"{BASE_URL}/api/auth/register", json=test_user_2, timeout=5)
        if response.status_code not in [200, 201]:
            print_test("Create Second User", False, f"Status: {response.status_code}")
            return False
        
        # Login to get user ID
        login_data = {"email": test_user_2["email"], "password": test_user_2["password"]}
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data, timeout=5)
        if response.status_code != 200:
            print_test("Login Second User", False, f"Status: {response.status_code}")
            return False
        
        user_2_id = response.json().get('user', {}).get('id')
        print_test("Create Second User", True, f"User ID: {user_2_id}")
        
        # Add member to group
        member_data = {"user_id": user_2_id}
        response = requests.post(
            f"{BASE_URL}/api/groups/{group_id}/members",
            json=member_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print_test("Add Member to Group", True, f"Added user {user_2_id} to group {group_id}")
            return True
        else:
            print_test("Add Member to Group", False, 
                      f"Status: {response.status_code}\nResponse: {response.text}")
            return False
            
    except Exception as e:
        print_test("Add Member to Group", False, f"Error: {str(e)}")
        return False

def test_add_recipe_to_group(auth_data, group_id, recipe_id):
    """Test adding a recipe to a group"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("TESTING ADD RECIPE TO GROUP")
    print(f"{'='*60}{Colors.END}\n")
    
    if not auth_data or not group_id or not recipe_id:
        print_test("Add Recipe to Group", False, "Missing required data")
        return False
    
    headers = {"Authorization": f"Bearer {auth_data['token']}"}
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/groups/{group_id}/recipes/{recipe_id}",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print_test("Add Recipe to Group", True, 
                      f"Added recipe {recipe_id} to group {group_id}")
            return True
        else:
            print_test("Add Recipe to Group", False, 
                      f"Status: {response.status_code}\nResponse: {response.text}")
            return False
            
    except Exception as e:
        print_test("Add Recipe to Group", False, f"Error: {str(e)}")
        return False

def test_cors():
    """Test CORS configuration"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("TESTING CORS CONFIGURATION")
    print(f"{'='*60}{Colors.END}\n")
    
    try:
        # Test preflight request from frontend origin
        headers = {
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type, Authorization"
        }
        
        response = requests.options(f"{BASE_URL}/api/recipes/", headers=headers, timeout=5)
        
        cors_headers = {
            "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
            "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
            "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers"),
        }
        
        print(f"  CORS Headers: {json.dumps(cors_headers, indent=2)}")
        
        if cors_headers["Access-Control-Allow-Origin"]:
            print_test("CORS Configuration", True, "CORS headers present")
            return True
        else:
            print_test("CORS Configuration", False, "No CORS headers found")
            return False
            
    except Exception as e:
        print_test("CORS Configuration", False, f"Error: {str(e)}")
        return False

def main():
    print(f"\n{Colors.YELLOW}{'='*60}")
    print("RECIPE ROOM API DIAGNOSTIC TEST")
    print(f"{'='*60}{Colors.END}\n")
    
    # Test 1: API Health
    if not test_api_health():
        print(f"\n{Colors.RED}API is not running. Stopping tests.{Colors.END}\n")
        return
    
    # Test 2: CORS
    test_cors()
    
    # Test 3: Authentication
    auth_data = test_auth_flow()
    
    # Test 4: Recipe Creation
    recipe_id = test_recipe_creation(auth_data)
    
    # Test 5: Group Creation
    group_id = test_group_creation(auth_data)
    
    # Test 6: Add Member to Group
    test_add_member_to_group(auth_data, group_id)
    
    # Test 7: Add Recipe to Group
    test_add_recipe_to_group(auth_data, group_id, recipe_id)
    
    # Summary
    print(f"\n{Colors.YELLOW}{'='*60}")
    print("DIAGNOSTIC TEST COMPLETE")
    print(f"{'='*60}{Colors.END}\n")
    
    print(f"{Colors.BLUE}Next Steps:{Colors.END}")
    print("1. Check if frontend is pointing to http://localhost:8000")
    print("2. Verify frontend is sending correct data format")
    print("3. Check browser console for CORS errors")
    print("4. Ensure JWT tokens are being stored and sent correctly")
    print()

if __name__ == "__main__":
    main()
