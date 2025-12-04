from flask import Flask, redirect, url_for
from config import Config
from flask_login import LoginManager
from extensions import db, csrf
from app.models import User

def create_app(config_class: type[Config] = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    
    # optional settings
    
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"
    
    
    #This function tells Flask-Login how to load a user from seesion
    @login_manager.user_loader
    def load_user(user_id: int) -> User | None:
        return User.query.get(int(user_id))
    
    #Register blueprints
    from app.routes.user_routes import user_bp
    from app.routes.role_routes import role_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.permission_routes import permission_bp
    
    app.register_blueprint(user_bp)
    app.register_blueprint(role_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(permission_bp)
    
    # Add this block so "/" goes to the Users list
    @app.route("/")
    def home():
        return redirect(url_for("users.index"))
    
    #Create tables
    with app.app_context():
        from app.models import User, Role, Permission
        db.create_all()
        
    return app