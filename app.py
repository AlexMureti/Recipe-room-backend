from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from dotenv import load_dotenv
from models import db

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    CORS(app)
    
    from routes.auth import auth_bp
    from routes.search import search_bp
    from routes.payments import payment_bp
    from routes.recipes import recipe_bp
    from routes.groups import group_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(payment_bp, url_prefix='/api/payments')
    app.register_blueprint(recipe_bp, url_prefix='/api/recipes')
    app.register_blueprint(group_bp, url_prefix='/api/groups')
    
    # API root endpoint for discovery
    @app.route('/')
    def api_root():
        return jsonify({
            'name': 'Recipe Room API',
            'version': '1.0.0',
            'description': 'Backend API for Recipe Room application',
            'endpoints': {
                'auth': '/api/auth',
                'search': '/api/search',
                'recipes': '/api/recipes',
                'groups': '/api/groups',
                'payments': '/api/payments'
            },
            'documentation': '/api-docs'
        }), 200
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'recipe-room-api'
        }), 200
    
    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)