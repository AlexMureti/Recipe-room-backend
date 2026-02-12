# TODO: Fix All Endpoints

## Step 1: Fix app.py - Register missing blueprints
- [x] Import and register recipes_bp with url_prefix '/api/recipes'
- [x] Import and register groups_bp with url_prefix '/api/groups'  
- [x] Fix search_bp url_prefix from '/api' to '/api/search'

## Step 2: Consolidate recipe routes in routes/recipes.py
- [x] Add missing discover, rate, rating, bookmark routes from search.py to recipes.py

## Step 3: Clean up routes/search.py
- [x] Remove recipe routes from search.py (keep only search functionality)
- [x] Fix url_prefix to '/api/search'

## Step 4: Fix test_endpoints.py
- [x] Change BASE URL from 5000 to 8000

## Step 5: Test all endpoints
- [x] Run app.py and verify all endpoints work


