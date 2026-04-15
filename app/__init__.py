import os
import logging
from flask import Flask
from flasgger import Swagger
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_dance.contrib.google import make_google_blueprint
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_bcrypt import Bcrypt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from extensions import db, mail, csrf, limiter, bcrypt

# Modular Imports
from models import User, Bug # Import models to ensure they are registered
from routes import main_bp, admin_bp, analytics_bp, api_bp
from config import Config


def create_app(config_class=Config):
    load_dotenv()
    
    app = Flask(__name__, 
                template_folder='../templates', 
                static_folder='../static')

    # Handle proxy headers (necessary for HTTPS on Render/Heroku)
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    app.config.from_object(config_class)
    
    db.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    bcrypt.init_app(app)
    
    # Swagger initialization
    if not os.environ.get('VERCEL') or os.environ.get('ENABLE_SWAGGER') == 'True':
        Swagger(app)
    else:
        logger.info("Skipping Swagger initialization.")

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # Google OAuth Configuration
    google_bp = make_google_blueprint(
        client_id=app.config.get("GOOGLE_CLIENT_ID"),
        client_secret=app.config.get("GOOGLE_CLIENT_SECRET"),
        scope=["profile", "email"],
        offline=True,
        redirect_to="main.google_authorized"
    )
    app.register_blueprint(google_bp, url_prefix="/")


    # Automatically create tables in the database
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")

    return app


    return app
