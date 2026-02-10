from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Book, Review, db
from sqlalchemy.orm import joinedload

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('auth.register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful!')
        return redirect(url_for('auth.login'))

    return render_template("register.html")

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            if user.is_banned:
                flash('Your account has been banned. Please contact the administrator.')
                return redirect(url_for('auth.login'))
            
            login_user(user)
            
            # Redirect admin to admin dashboard
            if user.is_admin():
                return redirect(url_for('admin.admin_dashboard'))
            
            return redirect(url_for('auth.dashboard'))

        flash('Invalid username or password')
    return render_template("login.html")

@auth_bp.route("/user/logout")
@login_required
def user_logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route("/profile")
@login_required
def profile():
    return redirect(url_for('auth.user_profile'))

@auth_bp.route("/user/profile")
@login_required
def user_profile():
    return render_template("profile.html", user=current_user)

@auth_bp.route("/user/dashboard")
@login_required
def dashboard():
    # Get user stats
    total_books_added = Book.query.filter_by(submitted_by=current_user.id).count()
    total_reviews_written = Review.query.filter_by(user_id=current_user.id).count()
    recent_books = Book.query.filter_by(submitted_by=current_user.id).order_by(Book.created_at.desc()).limit(5).all()
    recent_reviews = Review.query.filter_by(user_id=current_user.id).options(joinedload(Review.book)).order_by(Review.created_at.desc()).limit(5).all()
    
    return render_template("dashboard.html", 
                         user=current_user,
                         total_books_added=total_books_added,
                         total_reviews_written=total_reviews_written,
                         recent_books=recent_books,
                         recent_reviews=recent_reviews)

@auth_bp.route("/user/change-password", methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not current_user.check_password(current_password):
            flash('Current password is incorrect.')
            return redirect(url_for('auth.change_password'))
        
        if new_password != confirm_password:
            flash('New passwords do not match.')
            return redirect(url_for('auth.change_password'))
        
        if len(new_password) < 6:
            flash('New password must be at least 6 characters long.')
            return redirect(url_for('auth.change_password'))
        
        current_user.set_password(new_password)
        db.session.commit()
        flash('Password changed successfully!')
        return redirect(url_for('auth.dashboard'))
    
    return render_template("change_password.html", user=current_user)
