import os

class Config:
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///recipe_room.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS Configuration
    # Comma-separated list of allowed origins for production
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Environment
    ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # PayD API Configuration
    PAYD_API_URL = "https://api.payd.money"
    PAYD_USERNAME = os.environ.get('PAYD_USERNAME')
    PAYD_PASSWORD = os.environ.get('PAYD_PASSWORD')
    PAYD_API_SECRET = os.environ.get('PAYD_API_SECRET')
    PAYD_ACCOUNT_USERNAME = os.environ.get('PAYD_ACCOUNT_USERNAME')
    
    # Cloudinary Configuration
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')