from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from sqlalchemy.orm import DeclarativeBase

# Base model class for SQLAlchemy
class Base(DeclarativeBase):
    pass

# Initialize extensions (but don't bind to app yet)
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
mail = Mail()