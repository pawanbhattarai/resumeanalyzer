import os
import logging
from dotenv import load_dotenv

from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from extensions import db, login_manager, mail

# Load environment variables from .env
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def create_app():
    # Create Flask app
    app = Flask(__name__)
    
    # App configuration from environment variables
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///resume_analyzer.db")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Mail configuration
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@resumeanalyzer.com')

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    CORS(app)

    # Login manager settings
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    with app.app_context():
        # Import models so SQLAlchemy can register them
        import models  # noqa: F401

        # Create database tables if they don't exist
        db.create_all()

        # User loader callback for Flask-Login
        @login_manager.user_loader
        def load_user(user_id):
            from models import User
            return User.query.get(int(user_id))

        # Register blueprints
        from auth import auth
        app.register_blueprint(auth, url_prefix='/auth')

        # Import and register routes
        from routes import register_routes
        register_routes(app)

    return app

# Create app instance
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)