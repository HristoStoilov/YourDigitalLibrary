"""
YourDigitalLibrary Application
Main application entry point following MVC architecture.
"""
import os
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from config import config
from models import db, User


def create_app(config_name=None):
    # Initialize Flask app
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    mail = Mail(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints (controllers)
    from controllers.main_controller import main_bp
    from controllers.auth_controller import auth_bp
    from controllers.book_controller import book_bp
    from controllers.review_controller import review_bp
    from controllers.admin_controller import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(admin_bp)
    
    return app


# Create application instance
app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@library.com', role='admin')
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
    
    app.run(debug=True)