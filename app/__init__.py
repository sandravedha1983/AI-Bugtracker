import os
import logging
from flask import Flask, render_template, jsonify, request
from flasgger import Swagger
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_dance.contrib.google import make_google_blueprint
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

# Import extensions and config
from .extensions import db, mail, csrf, limiter, bcrypt, migrate
from .models import User, Bug
from .routes.main import main_bp
from .routes.admin import admin_bp
from .routes.analytics import analytics_bp
from .api.routes import api_bp
from config import Config

def create_app(config_class=Config):
    load_dotenv()
    
    # Paths are now relative to this file
    app = Flask(__name__, 
                template_folder='templates', 
                static_folder='static')

    app.config.from_object(config_class)
    
    # Critical for Render: Handle HTTPS proxy headers
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    from .middleware.security import add_security_headers
    app.after_request(add_security_headers)

    # Configure Logging
    if not app.debug:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        ))
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)
    
    app.logger.info("Initializing Bug Tracker App in production-ready mode...")

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    bcrypt.init_app(app)
    
    # Swagger initialization
    if app.config.get('DEBUG') or os.environ.get('ENABLE_SWAGGER') == 'True':
        Swagger(app)

    # Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.error(f"404 Error: {error} at {request.url}")
        if request.path.startswith('/api/'):
            return jsonify(error="Not Found", message="The requested resource was not found"), 404
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"500 Error: {error} at {request.url}")
        db.session.rollback()
        if request.path.startswith('/api/'):
            return jsonify(error="Internal Server Error", message="An unexpected error occurred"), 500
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        app.logger.warning(f"403 Error: {error} at {request.url}")
        if request.path.startswith('/api/'):
            return jsonify(error="Forbidden", message="You do not have permission to access this resource"), 403
        return render_template('errors/403.html'), 403

    @app.errorhandler(429)
    def ratelimit_handler(e):
        app.logger.warning(f"Rate limit exceeded: {e} at {request.url}")
        return jsonify(error="Rate Limit Exceeded", message=str(e.description)), 429

    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Unhandled Exception: {str(e)}", exc_info=True)
        db.session.rollback()
        if request.path.startswith('/api/'):
            return jsonify(error="Internal Server Error", message="A critical error occurred"), 500
        return render_template('errors/500.html'), 500

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # Google OAuth
    if app.config.get("GOOGLE_CLIENT_ID"):
        google_bp = make_google_blueprint(
            client_id=app.config.get("GOOGLE_CLIENT_ID"),
            client_secret=app.config.get("GOOGLE_CLIENT_SECRET"),
            scope=["profile", "email"],
            offline=True,
            redirect_to="main.google_authorized"
        )
        app.register_blueprint(google_bp, url_prefix="/login")
    else:
        app.logger.warning("GOOGLE_CLIENT_ID not set. Google OAuth will be disabled.")

    # Database and Seed Data
    with app.app_context():
        try:
            db.create_all()
            app.logger.info("Database tables verified.")
            
            from .utils.seeds import seed_database
            seed_database(app)

        except Exception as e:
            app.logger.error(f"Startup Database Error: {str(e)}")

    return app
