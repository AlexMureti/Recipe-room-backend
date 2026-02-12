"""
Recipe-Room Backend - Search Routes
Author: Alex Maingi

Flask Blueprint for search functionality.
Prefix: /api/search
"""

from flask import Blueprint, request, jsonify
from sqlalchemy import func
from models import db, Recipe, Rating

search_bp = Blueprint('search', __name__)

@search_bp.route('/recipes', methods=['GET'])
def search_recipes():
    """
    Search recipes with various filters.
    Query params: name, ingredient, people_served, country, rating
    Public endpoint - no authentication required
    """
    try:
        query = Recipe.query.filter_by(recipe_is_deleted=False)
        
        # Filter by name (searches in title)
        if name := request.args.get('name'):
            query = query.filter(Recipe.recipe_title.ilike(f'%{name}%'))
        
        # Filter by ingredient
        if ingredient := request.args.get('ingredient'):
            query = query.filter(Recipe.recipe_ingredients.ilike(f'%{ingredient}%'))
        
        # Filter by people served
        if people := request.args.get('people_served'):
            query = query.filter(Recipe.recipe_people_served == int(people))
        
        # Filter by country
        if country := request.args.get('country'):
            query = query.filter(Recipe.recipe_country == country)
        
        # Filter by minimum rating
        if rating := request.args.get('rating'):
            query = query.join(Rating).group_by(Recipe.recipe_id).having(
                func.avg(Rating.rating_value) >= float(rating)
            )
        
        # Order by newest first
        recipes = query.order_by(Recipe.recipe_created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'count': len(recipes),
            'recipes': [recipe.to_dict(include_owner=True, include_stats=True) for recipe in recipes]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Search failed',
            'message': str(e)
        }), 500

