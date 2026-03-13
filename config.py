import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-12345')
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    
    if not SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Connection Stability for Neon PostgreSQL
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20
    }

    # Session & Cookie Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

    # Mail Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'AI Bug Tracker <noreply@gmail.com>')
    MAIL_DEBUG = True
    
    # Admin & Security
    ADMIN_PASSWORD_HASH = os.environ.get('ADMIN_PASSWORD_HASH')
    
    # GitHub Integration
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
    GITHUB_REPO = os.environ.get('GITHUB_REPO')
    GITHUB_OWNER = os.environ.get('GITHUB_OWNER')
    
    # Google OAuth
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
