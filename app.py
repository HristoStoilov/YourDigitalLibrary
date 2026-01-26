from flask import Flask
from flask_scss import Scss
from flask_login import LoginManager
from models import db, User

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# Compile SCSS
Scss(app, static_dir='static', asset_dir='assets')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
from routes.main_routes import main_bp
from routes.auth_routes import auth_bp
from routes.book_routes import book_bp
from routes.review_routes import review_bp

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(book_bp)
app.register_blueprint(review_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)