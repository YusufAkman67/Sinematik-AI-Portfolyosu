from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Redirect target for unauthorized access
csrf = CSRFProtect()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Load configuration settings
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Bind extensions to app context
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Register models
    from . import models
    
    # Register Blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from .errors import errors as errors_blueprint
    app.register_blueprint(errors_blueprint)
    
    return app
