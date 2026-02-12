"""
Recipe-Room Backend - Comment Routes
Derrick's responsibility

Flask Blueprint for all comment-related API endpoints.
Prefix: /api/comments
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from models import Comment, Recipe, User
from database import db

# Setup blueprint
comment_bp = Blueprint('comments', __name__, url_prefix='/api/comments')


@comment_bp.route('/recipe/<int:recipe_id>', methods=['GET'])
def get_recipe_comments(recipe_id):
    """
    Get all comments for a specific recipe.
    Public endpoint - no authentication required
    Query params: page, per_page
    """
    try:
        # Check if recipe exists
        recipe = Recipe.query.filter_by(recipe_id=recipe_id, recipe_is_deleted=False).first()
        if not recipe:
            return jsonify({
                'success': False,
                'error': 'Recipe not found'
            }), 404
        
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Get comments (newest first)
        comments_query = Comment.query.filter_by(
            recipe_id=recipe_id,
            is_deleted=False
        ).order_by(Comment.created_at.desc())
        
        # Paginate
        paginated_comments = comments_query.paginate(
            page=page,
            per_page=min(per_page, 100),
            error_out=False
        )
        
        comments_list = [comment.to_dict() for comment in paginated_comments.items]
        
        return jsonify({
            'success': True,
            'comments': comments_list,
            'pagination': {
                'current_page': paginated_comments.page,
                'total_pages': paginated_comments.pages,
                'total_items': paginated_comments.total,
                'per_page': per_page
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve comments',
            'message': str(e)
        }), 500


@comment_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment():
    """
    Create a new comment on a recipe.
    Requires authentication.
    Expected JSON: {"recipe_id": 123, "comment_text": "Great recipe!"}
    """
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # Validate input
        recipe_id = data.get('recipe_id')
        comment_text = data.get('comment_text', '').strip()
        
        if not recipe_id:
            return jsonify({
                'success': False,
                'error': 'Validation failed',
                'message': 'recipe_id is required'
            }), 400
        
        if not comment_text:
            return jsonify({
                'success': False,
                'error': 'Validation failed',
                'message': 'comment_text cannot be empty'
            }), 400
        
        # Check if recipe exists
        recipe = Recipe.query.filter_by(recipe_id=recipe_id, recipe_is_deleted=False).first()
        if not recipe:
            return jsonify({
                'success': False,
                'error': 'Recipe not found'
            }), 404
        
        # Create comment
        new_comment = Comment(
            recipe_id=recipe_id,
            user_id=current_user_id,
            comment_text=comment_text
        )
        
        db.session.add(new_comment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Comment created successfully',
            'comment': new_comment.to_dict()
        }), 201
        
    except SQLAlchemyError as db_error:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Database error',
            'message': str(db_error)
        }), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to create comment',
            'message': str(e)
        }), 500


@comment_bp.route('/<int:comment_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment(comment_id):
    """
    Update a comment.
    Only the comment author can update it.
    """
    try:
        current_user_id = int(get_jwt_identity())
        
        # Find comment
        comment = Comment.query.filter_by(id=comment_id, is_deleted=False).first()
        if not comment:
            return jsonify({
                'success': False,
                'error': 'Comment not found'
            }), 404
        
        # Check if user owns the comment
        if comment.user_id != current_user_id:
            return jsonify({
                'success': False,
                'error': 'Permission denied',
                'message': 'You can only edit your own comments'
            }), 403
        
        # Get update data
        data = request.get_json()
        comment_text = data.get('comment_text', '').strip()
        
        if not comment_text:
            return jsonify({
                'success': False,
                'error': 'Validation failed',
                'message': 'comment_text cannot be empty'
            }), 400
        
        # Update comment
        comment.comment_text = comment_text
        comment.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Comment updated successfully',
            'comment': comment.to_dict()
        }), 200
        
    except SQLAlchemyError as db_error:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Database error',
            'message': str(db_error)
        }), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to update comment',
            'message': str(e)
        }), 500


@comment_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    """
    Delete a comment (soft delete).
    Only the comment author can delete it.
    """
    try:
        current_user_id = int(get_jwt_identity())
        
        # Find comment
        comment = Comment.query.filter_by(id=comment_id, is_deleted=False).first()
        if not comment:
            return jsonify({
                'success': False,
                'error': 'Comment not found'
            }), 404
        
        # Check if user owns the comment
        if comment.user_id != current_user_id:
            return jsonify({
                'success': False,
                'error': 'Permission denied',
                'message': 'You can only delete your own comments'
            }), 403
        
        # Soft delete
        comment.is_deleted = True
        comment.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Comment deleted successfully'
        }), 200
        
    except SQLAlchemyError as db_error:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Database error',
            'message': str(db_error)
        }), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to delete comment',
            'message': str(e)
        }), 500
