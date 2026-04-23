import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Basic Config
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-key-for-dev-only-replace-on-render')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Critical for production logs on Render
    PROPAGATE_EXCEPTIONS = True
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    
    if not SQLALCHEMY_DATABASE_URI:
        # Fallback for local dev if DATABASE_URL is missing
        SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Connection Pool Management (Postgres optimized)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20
    }
    
    # Session & Cookie Security
    # On Render, HTTPS is handled by proxy, make sure cookies are secure
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', str(not DEBUG)).lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=12)

    # Mail Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'Bug Tracker <noreply@bugtracker.com>')
    
    # Google OAuth
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
    
    # Rate Limiting
    # Relax limits for production if causing false positives
    RATELIMIT_DEFAULT = "200 per day; 50 per hour"
    RATELIMIT_STRATEGY = 'fixed-window'
