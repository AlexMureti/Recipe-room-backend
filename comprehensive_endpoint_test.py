#!/usr/bin/env python3
"""
Comprehensive Endpoint Testing Script for Recipe Room API
Tests all endpoints to verify they're working correctly
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

# ANSI color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# Test results tracking
results = {
    'passed': 0,
    'failed': 0,
    'errors': []
}

def log_test(name, passed, status_code=None, message=""):
    """Log test result with color coding"""
    if passed:
        print(f"{GREEN}✓{RESET} {name} - Status: {status_code} {message}")
        results['passed'] += 1
    else:
        print(f"{RED}✗{RESET} {name} - Status: {status_code} {message}")
        results['failed'] += 1
        results['errors'].append(f"{name}: {message}")

def test_endpoint(method, url, expected_status, headers=None, json_data=None, files=None, description=""):
    """Generic endpoint tester"""
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            if files:
                response = requests.post(url, headers=headers, files=files)
            else:
                response = requests.post(url, headers=headers, json=json_data)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=json_data)
        elif method == 'PATCH':
            response = requests.patch(url, headers=headers, json=json_data)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, json=json_data)
        
        passed = response.status_code == expected_status
        log_test(
            description, 
            passed, 
            response.status_code,
            f"- Expected: {expected_status}"
        )
        
        return response
    except Exception as e:
        log_test(description, False, None, f"- Exception: {str(e)}")
        return None

print(f"\n{BLUE}{'='*80}{RESET}")
print(f"{BLUE}Recipe Room API Endpoint Testing{RESET}")
print(f"{BLUE}{'='*80}{RESET}\n")

# Store token for authenticated requests
token = None
user_id = None
recipe_id = None
group_id = None

print(f"\n{YELLOW}=== ROOT ENDPOINTS ==={RESET}\n")

# 1. Test API Root
response = test_endpoint(
    'GET', BASE_URL, 200,
    description="GET / - API Root"
)

# 2. Test Health Check
response = test_endpoint(
    'GET', f"{BASE_URL}/health", 200,
    description="GET /health - Health Check"
)

print(f"\n{YELLOW}=== AUTH ENDPOINTS ==={RESET}\n")

# 3. Register User
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
test_user = {
    "username": f"testuser_{timestamp}",
    "email": f"test_{timestamp}@test.com",
    "password": "password123"
}

response = test_endpoint(
    'POST', f"{API_BASE}/auth/register", 201,
    json_data=test_user,
    description="POST /api/auth/register - Register User"
)

# 4. Login
response = test_endpoint(
    'POST', f"{API_BASE}/auth/login", 200,
    json_data={"email": test_user['email'], "password": test_user['password']},
    description="POST /api/auth/login - Login"
)

if response and response.status_code == 200:
    data = response.json()
    token = data.get('access_token')
    user_id = data.get('user', {}).get('id')
    print(f"  {BLUE}→ Token acquired for user ID: {user_id}{RESET}")

# 5. Get Profile
if token:
    headers = {"Authorization": f"Bearer {token}"}
    response = test_endpoint(
        'GET', f"{API_BASE}/auth/profile", 200,
        headers=headers,
        description="GET /api/auth/profile - Get Profile (authenticated)"
    )

# 6. Update Profile
if token:
    response = test_endpoint(
        'PUT', f"{API_BASE}/auth/profile", 200,
        headers=headers,
        json_data={"username": f"updated_{timestamp}"},
        description="PUT /api/auth/profile - Update Profile (authenticated)"
    )

# 7. Upload Profile Image (will fail without actual file, but tests endpoint existence)
if token:
    response = test_endpoint(
        'POST', f"{API_BASE}/auth/upload-image", 400,  # Expect 400 as no image provided
        headers=headers,
        description="POST /api/auth/upload-image - Upload Image Endpoint Check"
    )

print(f"\n{YELLOW}=== RECIPE ENDPOINTS ==={RESET}\n")

# 8. Get All Recipes
response = test_endpoint(
    'GET', f"{API_BASE}/recipes/", 200,
    description="GET /api/recipes/ - Get All Recipes (public)"
)

# 9. Create Recipe
if token:
    new_recipe = {
        "title": f"Test Recipe {timestamp}",
        "description": "A delicious test recipe",
        "country": "Kenya",
        "ingredients": [
            {"name": "Flour", "quantity": "2 cups"},
            {"name": "Sugar", "quantity": "1 cup"}
        ],
        "procedure": [
            {"step": 1, "instruction": "Mix flour and sugar together"},
            {"step": 2, "instruction": "Bake at 350F for 30 minutes"}
        ],
        "people_served": 4,
        "prep_time": 15,
        "cook_time": 30
    }
    
    response = test_endpoint(
        'POST', f"{API_BASE}/recipes/", 201,
        headers=headers,
        json_data=new_recipe,
        description="POST /api/recipes/ - Create Recipe (authenticated)"
    )
    
    if response and response.status_code == 201:
        recipe_id = response.json().get('recipe', {}).get('recipe_id')
        print(f"  {BLUE}→ Recipe created with ID: {recipe_id}{RESET}")

# 10. Get Single Recipe
if recipe_id:
    response = test_endpoint(
        'GET', f"{API_BASE}/recipes/{recipe_id}", 200,
        description=f"GET /api/recipes/{recipe_id} - Get Single Recipe (public)"
    )

# 11. Update Recipe
if token and recipe_id:
    response = test_endpoint(
        'PUT', f"{API_BASE}/recipes/{recipe_id}", 200,
        headers=headers,
        json_data={"title": f"Updated Recipe {timestamp}"},
        description=f"PUT /api/recipes/{recipe_id} - Update Recipe (authenticated)"
    )

# 12. Get Recipe Edit History
if token and recipe_id:
    response = test_endpoint(
        'GET', f"{API_BASE}/recipes/{recipe_id}/history", 200,
        headers=headers,
        description=f"GET /api/recipes/{recipe_id}/history - Get Edit History (authenticated)"
    )

# 13. Get Recipes by User
if user_id:
    response = test_endpoint(
        'GET', f"{API_BASE}/recipes/user/{user_id}", 200,
        description=f"GET /api/recipes/user/{user_id} - Get User's Recipes (public)"
    )

# 14. Discover Recipes (with filters)
response = test_endpoint(
    'GET', f"{API_BASE}/recipes/discover", 200,
    description="GET /api/recipes/discover - Discover Recipes (public)"
)

# 15. Discover Recipes with filter
response = test_endpoint(
    'GET', f"{API_BASE}/recipes/discover?name=test", 200,
    description="GET /api/recipes/discover?name=test - Discover with Filter (public)"
)

# 16. Rate Recipe
if token and recipe_id:
    response = test_endpoint(
        'POST', f"{API_BASE}/recipes/{recipe_id}/rate", 200,
        headers=headers,
        json_data={"value": 5},
        description=f"POST /api/recipes/{recipe_id}/rate - Rate Recipe (authenticated)"
    )

# 17. Get Recipe Rating
if recipe_id:
    response = test_endpoint(
        'GET', f"{API_BASE}/recipes/{recipe_id}/rating", 200,
        description=f"GET /api/recipes/{recipe_id}/rating - Get Recipe Rating (public)"
    )

# 18. Bookmark Recipe
if token and recipe_id:
    response = test_endpoint(
        'POST', f"{API_BASE}/recipes/{recipe_id}/bookmark", 201,
        headers=headers,
        description=f"POST /api/recipes/{recipe_id}/bookmark - Bookmark Recipe (authenticated)"
    )

# 19. Remove Bookmark
if token and recipe_id:
    response = test_endpoint(
        'DELETE', f"{API_BASE}/recipes/{recipe_id}/bookmark", 200,
        headers=headers,
        description=f"DELETE /api/recipes/{recipe_id}/bookmark - Remove Bookmark (authenticated)"
    )

print(f"\n{YELLOW}=== SEARCH ENDPOINTS ==={RESET}\n")

# 20. Search Recipes
response = test_endpoint(
    'GET', f"{API_BASE}/search/recipes", 200,
    description="GET /api/search/recipes - Search Recipes (public)"
)

# 21. Search Recipes with filter
response = test_endpoint(
    'GET', f"{API_BASE}/search/recipes?ingredient=flour", 200,
    description="GET /api/search/recipes?ingredient=flour - Search with Filter (public)"
)

print(f"\n{YELLOW}=== GROUP ENDPOINTS ==={RESET}\n")

# 22. Get User Groups
if token:
    response = test_endpoint(
        'GET', f"{API_BASE}/groups/", 200,
        headers=headers,
        description="GET /api/groups/ - Get User Groups (authenticated)"
    )

# 23. Create Group
if token:
    new_group = {
        "name": f"Test Group {timestamp}",
        "description": "A test recipe group",
        "max_members": 10
    }
    
    response = test_endpoint(
        'POST', f"{API_BASE}/groups/", 201,
        headers=headers,
        json_data=new_group,
        description="POST /api/groups/ - Create Group (authenticated)"
    )
    
    if response and response.status_code == 201:
        group_id = response.json().get('group', {}).get('group_id')
        print(f"  {BLUE}→ Group created with ID: {group_id}{RESET}")

# 24. Get Group by ID
if token and group_id:
    response = test_endpoint(
        'GET', f"{API_BASE}/groups/{group_id}", 200,
        headers=headers,
        description=f"GET /api/groups/{group_id} - Get Group by ID (authenticated)"
    )

# 25. Update Group
if token and group_id:
    response = test_endpoint(
        'PUT', f"{API_BASE}/groups/{group_id}", 200,
        headers=headers,
        json_data={"description": "Updated description"},
        description=f"PUT /api/groups/{group_id} - Update Group (authenticated)"
    )

# 26. Get Group Recipes
if token and group_id:
    response = test_endpoint(
        'GET', f"{API_BASE}/groups/{group_id}/recipes", 200,
        headers=headers,
        description=f"GET /api/groups/{group_id}/recipes - Get Group Recipes (authenticated)"
    )

# 27. Add Recipe to Group
if token and group_id and recipe_id:
    response = test_endpoint(
        'POST', f"{API_BASE}/groups/{group_id}/recipes/{recipe_id}", 200,
        headers=headers,
        description=f"POST /api/groups/{group_id}/recipes/{recipe_id} - Add Recipe to Group (authenticated)"
    )

# 28. Remove Recipe from Group
if token and group_id and recipe_id:
    response = test_endpoint(
        'DELETE', f"{API_BASE}/groups/{group_id}/recipes/{recipe_id}", 200,
        headers=headers,
        description=f"DELETE /api/groups/{group_id}/recipes/{recipe_id} - Remove Recipe from Group (authenticated)"
    )

# Note: Skipping member add/remove as we'd need another user

print(f"\n{YELLOW}=== PAYMENT ENDPOINTS ==={RESET}\n")

# 29. Initiate Payment (will likely fail due to missing credentials, but tests endpoint)
if token:
    payment_data = {
        "amount": 100,
        "phone_number": "254712345678",
        "currency": "KES"
    }
    # Expect 500 or 400 due to missing PayD credentials
    response = requests.post(
        f"{API_BASE}/payments/initiate",
        headers=headers,
        json=payment_data
    )
    # Don't test for specific status as it depends on PayD config
    print(f"{BLUE}ℹ{RESET}  POST /api/payments/initiate - Payment Initiation Endpoint Check - Status: {response.status_code}")

print(f"\n{YELLOW}=== CLEANUP: DELETE RECIPE ==={RESET}\n")

# 30. Delete Recipe (cleanup)
if token and recipe_id:
    response = test_endpoint(
        'DELETE', f"{API_BASE}/recipes/{recipe_id}", 200,
        headers=headers,
        description=f"DELETE /api/recipes/{recipe_id} - Delete Recipe (authenticated)"
    )

# 31. Delete Group (cleanup)
if token and group_id:
    response = test_endpoint(
        'DELETE', f"{API_BASE}/groups/{group_id}", 200,
        headers=headers,
        description=f"DELETE /api/groups/{group_id} - Delete Group (authenticated)"
    )

# Summary
print(f"\n{BLUE}{'='*80}{RESET}")
print(f"{BLUE}Test Summary{RESET}")
print(f"{BLUE}{'='*80}{RESET}\n")
print(f"{GREEN}Passed:{RESET} {results['passed']}")
print(f"{RED}Failed:{RESET} {results['failed']}")
print(f"{BLUE}Total:{RESET}  {results['passed'] + results['failed']}\n")

if results['errors']:
    print(f"{RED}Failed Tests:{RESET}")
    for error in results['errors']:
        print(f"  - {error}")
    print()

if results['failed'] == 0:
    print(f"{GREEN}✓ All endpoints are working correctly!{RESET}\n")
else:
    print(f"{YELLOW}⚠ Some endpoints need attention{RESET}\n")
