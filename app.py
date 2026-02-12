from flask import Flask, jsonify, render_template_string
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from dotenv import load_dotenv
from models import db
from markupsafe import Markup
import markdown
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    
    # Initialize database tables on startup
    with app.app_context():
        db.create_all()
    
    # Configure CORS with proper origins
    cors_config = {
        'origins': app.config['CORS_ORIGINS'],
        'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
        'allow_headers': ['Content-Type', 'Authorization'],
        'supports_credentials': True
    }
    CORS(app, resources={r"/api/*": cors_config})
    
    from routes.auth import auth_bp
    from routes.search import search_bp
    from routes.payments import payment_bp
    from routes.recipes import recipe_bp
    from routes.groups import group_bp
    from routes.comments import comment_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(payment_bp, url_prefix='/api/payments')
    app.register_blueprint(recipe_bp, url_prefix='/api/recipes')
    app.register_blueprint(group_bp, url_prefix='/api/groups')
    app.register_blueprint(comment_bp, url_prefix='/api/comments')
    
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
                'payments': '/api/payments',
                'comments': '/api/comments'
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
    
    # API Documentation endpoints
    @app.route('/docs')
    @app.route('/api-docs')
    def api_documentation():
        """Serve API documentation as HTML"""
        try:
            # Read the markdown file
            docs_path = os.path.join(os.path.dirname(__file__), 'API_DOCUMENTATION.md')
            with open(docs_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Convert markdown to HTML
            html_content = Markup(markdown.markdown(
                md_content,
                extensions=['fenced_code', 'tables', 'toc']
            ))
            
            # HTML template with styling
            html_template = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Recipe Room API Documentation</title>
                <style>
                    * {
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        background: #f5f5f5;
                        padding: 20px;
                    }
                    .container {
                        max-width: 1000px;
                        margin: 0 auto;
                        background: white;
                        padding: 40px;
                        border-radius: 8px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    }
                    h1 {
                        color: #2c3e50;
                        border-bottom: 3px solid #3498db;
                        padding-bottom: 10px;
                        margin-bottom: 30px;
                        font-size: 2.5em;
                    }
                    h2 {
                        color: #34495e;
                        margin-top: 40px;
                        margin-bottom: 20px;
                        font-size: 1.8em;
                        border-bottom: 2px solid #ecf0f1;
                        padding-bottom: 8px;
                    }
                    h3 {
                        color: #555;
                        margin-top: 30px;
                        margin-bottom: 15px;
                        font-size: 1.3em;
                    }
                    p {
                        margin-bottom: 15px;
                    }
                    code {
                        background: #f4f4f4;
                        padding: 2px 6px;
                        border-radius: 3px;
                        font-family: 'Monaco', 'Courier New', monospace;
                        font-size: 0.9em;
                        color: #e74c3c;
                    }
                    pre {
                        background: #2c3e50;
                        color: #ecf0f1;
                        padding: 20px;
                        border-radius: 5px;
                        overflow-x: auto;
                        margin: 20px 0;
                        border-left: 4px solid #3498db;
                    }
                    pre code {
                        background: none;
                        color: #ecf0f1;
                        padding: 0;
                    }
                    ul, ol {
                        margin-left: 30px;
                        margin-bottom: 15px;
                    }
                    li {
                        margin-bottom: 8px;
                    }
                    strong {
                        color: #2c3e50;
                        font-weight: 600;
                    }
                    hr {
                        border: none;
                        border-top: 1px solid #ecf0f1;
                        margin: 30px 0;
                    }
                    .badge {
                        display: inline-block;
                        padding: 3px 8px;
                        border-radius: 3px;
                        font-size: 0.85em;
                        font-weight: bold;
                        margin-right: 8px;
                    }
                    .badge.post { background: #3498db; color: white; }
                    .badge.get { background: #2ecc71; color: white; }
                    .badge.put { background: #f39c12; color: white; }
                    .badge.delete { background: #e74c3c; color: white; }
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin: 20px 0;
                    }
                    th, td {
                        padding: 12px;
                        text-align: left;
                        border: 1px solid #ddd;
                    }
                    th {
                        background: #34495e;
                        color: white;
                        font-weight: 600;
                    }
                    tr:nth-child(even) {
                        background: #f9f9f9;
                    }
                    a {
                        color: #3498db;
                        text-decoration: none;
                    }
                    a:hover {
                        text-decoration: underline;
                    }
                    .header-info {
                        background: #ecf0f1;
                        padding: 15px;
                        border-radius: 5px;
                        margin-bottom: 30px;
                        border-left: 4px solid #3498db;
                    }
                    @media (max-width: 768px) {
                        .container {
                            padding: 20px;
                        }
                        h1 {
                            font-size: 2em;
                        }
                        h2 {
                            font-size: 1.5em;
                        }
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header-info">
                        <strong>🍳 Recipe Room API</strong> | 
                        <a href="/">Back to API Root</a> | 
                        <a href="/health">Health Check</a>
                    </div>
                    {{ content }}
                </div>
            </body>
            </html>
            """
            
            return render_template_string(html_template, content=html_content), 200
            
        except FileNotFoundError:
            return jsonify({
                'error': 'API documentation file not found'
            }), 404
        except Exception as e:
            return jsonify({
                'error': f'Failed to load documentation: {str(e)}'
            }), 500
    
    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)