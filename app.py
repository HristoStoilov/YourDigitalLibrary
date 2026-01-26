from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Compile SCSS
Scss(app, static_dir='static', asset_dir='assets')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile_picture = db.Column(db.String(300))
    bio = db.Column(db.Text)

    # Relationships
    reviews = db.relationship('Review', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    isbn = db.Column(db.String(13), unique=True)
    description = db.Column(db.Text)
    published_date = db.Column(db.Date)
    cover_image = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    submitted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    reviews = db.relationship('Review', backref='book', lazy=True)
    submitter = db.relationship('User', backref='books_submitted', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful!')
        return redirect(url_for('login'))

    return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))

        flash('Invalid username or password')
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@app.route("/books")
def books():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    author_filter = request.args.get('author', '')

    query = Book.query

    if search:
        query = query.filter(Book.title.contains(search))
    if author_filter:
        query = query.filter(Book.author.contains(author_filter))

    books = query.paginate(page=page, per_page=10)
    return render_template("books.html", books=books, search=search, author_filter=author_filter)

@app.route("/book/<int:book_id>")
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    reviews = Review.query.filter_by(book_id=book_id).all()
    return render_template("book_detail.html", book=book, reviews=reviews)

@app.route("/add_book", methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        isbn = request.form.get('isbn')
        description = request.form.get('description')
        published_date_str = request.form.get('published_date')

        published_date = None
        if published_date_str:
            published_date = datetime.strptime(published_date_str, '%Y-%m-%d').date()

        book = Book(
            title=title,
            author=author,
            isbn=isbn,
            description=description,
            published_date=published_date,
            submitted_by=current_user.id
        )
        db.session.add(book)
        db.session.commit()

        flash('Book added successfully!')
        return redirect(url_for('books'))

    return render_template("add_book.html")

@app.route("/edit_book/<int:book_id>", methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.submitted_by != current_user.id:
        flash('You do not have permission to edit this book.')
        return redirect(url_for('book_detail', book_id=book.id))
    
    if request.method == 'POST':
        book.title = request.form.get('title')
        book.author = request.form.get('author')
        book.isbn = request.form.get('isbn')
        book.description = request.form.get('description')
        published_date_str = request.form.get('published_date')
        if published_date_str:
            book.published_date = datetime.strptime(published_date_str, '%Y-%m-%d').date()

        db.session.commit()
        flash('Book updated successfully!')
        return redirect(url_for('book_detail', book_id=book.id))

    return render_template("edit_book.html", book=book)

@app.route("/delete_book/<int:book_id>", methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.submitted_by != current_user.id:
        flash('You do not have permission to delete this book.')
        return redirect(url_for('book_detail', book_id=book.id))
    
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!')
    return redirect(url_for('books'))

@app.route("/add_review/<int:book_id>", methods=['POST'])
@login_required
def add_review(book_id):
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment')

    review = Review(
        rating=rating,
        comment=comment,
        user_id=current_user.id,
        book_id=book_id
    )
    db.session.add(review)
    db.session.commit()

    flash('Review added successfully!')
    return redirect(url_for('book_detail', book_id=book_id))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)