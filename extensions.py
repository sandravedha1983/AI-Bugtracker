from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
mail = Mail()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])
bcrypt = Bcrypt()
