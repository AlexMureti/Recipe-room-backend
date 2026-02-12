import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

# Create user and login
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
test_user = {
    "username": f"debuguser_{timestamp}",
    "email": f"debug_{timestamp}@test.com",
    "password": "password123"
}

print("1. Registering user...")
r = requests.post(f"{BASE_URL}/auth/register", json=test_user)
print(f"Register: {r.status_code}")

print("\n2. Logging in...")
r = requests.post(f"{BASE_URL}/auth/login", json={"email": test_user['email'], "password": test_user['password']})
token = r.json().get('access_token')
headers = {"Authorization": f"Bearer {token}"}
print(f"Login: {r.status_code}, Token: {token[:20]}...")

print("\n3. Creating recipe...")
new_recipe = {
    "title": f"Debug Recipe {timestamp}",
    "ingredients": [{"name": "Flour", "quantity": "2 cups"}],
    "procedure": [{"step": 1, "instruction": "Mix ingredients"}],
    "people_served": 4
}
r = requests.post(f"{BASE_URL}/recipes/", headers=headers, json=new_recipe)
print(f"Create Recipe: {r.status_code}")
recipe_id = r.json().get('recipe', {}).get('recipe_id')
print(f"Recipe ID: {recipe_id}")

print("\n4. Creating group...")
new_group = {
    "name": f"Debug Group {timestamp}",
    "description": "A test group"
}
r = requests.post(f"{BASE_URL}/groups/", headers=headers, json=new_group)
print(f"Create Group: {r.status_code}")
group_id = r.json().get('group', {}).get('group_id')
print(f"Group ID: {group_id}")

print(f"\n5. Adding recipe {recipe_id} to group {group_id}...")
r = requests.post(f"{BASE_URL}/groups/{group_id}/recipes/{recipe_id}", headers=headers)
print(f"Add Recipe to Group: {r.status_code}")
print(f"Response: {json.dumps(r.json(), indent=2)}")
