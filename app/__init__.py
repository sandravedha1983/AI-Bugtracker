import os
import logging
from flask import Flask, render_template, jsonify
from flasgger import Swagger
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_dance.contrib.google import make_google_blueprint
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

# Import extensions
from extensions import db, mail, csrf, limiter, bcrypt
from models import User, Bug
from routes import main_bp, admin_bp, analytics_bp, api_bp
from config import Config

def create_app(config_class=Config):
    load_dotenv()
    
    # Use absolute paths for templates and static folders to ensure they load on Render
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(os.path.dirname(base_dir), 'templates')
    static_dir = os.path.join(os.path.dirname(base_dir), 'static')

    app = Flask(__name__, 
                template_folder=template_dir, 
                static_folder=static_dir)

    app.config.from_object(config_class)
    
    # Critical for Render: Handle HTTPS proxy headers
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # Configure Logging
    if not app.debug:
        logging.basicConfig(level=logging.INFO)
    
    app.logger.info("Initializing Bug Tracker App...")

    # Initialize Extensions
    db.init_app(app)
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
        app.logger.error(f"Page not found: {error}")
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Server Error: {error}")
        db.session.rollback()
        return render_template('errors/500.html'), 500

    @app.errorhandler(429)
    def ratelimit_handler(e):
        app.logger.warning(f"Rate limit exceeded: {e}")
        return jsonify(error="ratelimit exceeded", message=str(e.description)), 429

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # Google OAuth
    google_bp = make_google_blueprint(
        client_id=app.config.get("GOOGLE_CLIENT_ID"),
        client_secret=app.config.get("GOOGLE_CLIENT_SECRET"),
        scope=["profile", "email"],
        offline=True,
        redirect_to="main.google_authorized"
    )
    app.register_blueprint(google_bp, url_prefix="/")

    # Database and Seed Data
    with app.app_context():
        try:
            db.create_all()
            app.logger.info("Database tables verified.")
            
            # Seed default admin if missing
            admin_email = os.environ.get('ADMIN_EMAIL', 'admin@bugtracker.com')
            admin_user = User.query.filter_by(email=admin_email).first()
            if not admin_user:
                app.logger.info("Seeding default admin user...")
                from werkzeug.security import generate_password_hash
                new_admin = User(
                    name="System Admin",
                    email=admin_email,
                    role="admin",
                    is_verified=True
                )
                admin_pass = os.environ.get('ADMIN_PASSWORD', 'admin123')
                new_admin.set_password(admin_pass)
                db.session.add(new_admin)
                db.session.commit()
                app.logger.info("Admin user created successfully.")

        except Exception as e:
            app.logger.error(f"Startup Error: {str(e)}")

    return app
