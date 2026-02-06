from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import User, Book, Review, db
from sqlalchemy import func, Date
from datetime import datetime, timedelta
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You do not have permission to access this page.')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route("/<username>/admin/dashboard")
@login_required
@admin_required
def admin_dashboard(username):
    if current_user.username != username:
        return redirect(url_for('admin.admin_dashboard', username=current_user.username))
    
    # Get statistics
    total_users = User.query.count()
    total_books = Book.query.count()
    total_reviews = Review.query.count()
    banned_users = User.query.filter_by(is_banned=True).count()
    
    # Books added per day (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    books_per_day = db.session.query(
        func.date(Book.created_at).label('date'),
        func.count(Book.id).label('count')
    ).filter(Book.created_at >= seven_days_ago).group_by(
        func.date(Book.created_at)
    ).order_by(func.date(Book.created_at)).all()
    
    # Reviews per day (last 7 days)
    reviews_per_day = db.session.query(
        func.date(Review.created_at).label('date'),
        func.count(Review.id).label('count')
    ).filter(Review.created_at >= seven_days_ago).group_by(
        func.date(Review.created_at)
    ).order_by(func.date(Review.created_at)).all()
    
    # Recent users
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    
    # Recent books
    recent_books = Book.query.order_by(Book.created_at.desc()).limit(10).all()
    
    # Recent reviews
    recent_reviews = Review.query.order_by(Review.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_books=total_books,
                         total_reviews=total_reviews,
                         banned_users=banned_users,
                         books_per_day=books_per_day,
                         reviews_per_day=reviews_per_day,
                         recent_users=recent_users,
                         recent_books=recent_books,
                         recent_reviews=recent_reviews)

@admin_bp.route("/<username>/admin/users")
@login_required
@admin_required
def manage_users(username):
    if current_user.username != username:
        return redirect(url_for('admin.manage_users', username=current_user.username))
    
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = User.query
    if search:
        query = query.filter(User.username.contains(search))
    
    users = query.order_by(User.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/users.html', users=users, search=search)

@admin_bp.route("/<username>/admin/ban_user/<int:user_id>", methods=['POST'])
@login_required
@admin_required
def ban_user(username, user_id):
    if current_user.username != username:
        return redirect(url_for('admin.manage_users', username=current_user.username))
    
    user = User.query.get_or_404(user_id)
    
    if user.is_admin():
        flash('Cannot ban an admin user.')
        return redirect(url_for('admin.manage_users', username=username))
    
    user.is_banned = True
    db.session.commit()
    flash(f'User {user.username} has been banned.')
    return redirect(url_for('admin.manage_users', username=username))

@admin_bp.route("/<username>/admin/unban_user/<int:user_id>", methods=['POST'])
@login_required
@admin_required
def unban_user(username, user_id):
    if current_user.username != username:
        return redirect(url_for('admin.manage_users', username=current_user.username))
    
    user = User.query.get_or_404(user_id)
    user.is_banned = False
    db.session.commit()
    flash(f'User {user.username} has been unbanned.')
    return redirect(url_for('admin.manage_users', username=username))

@admin_bp.route("/<username>/admin/reviews")
@login_required
@admin_required
def manage_reviews(username):
    if current_user.username != username:
        return redirect(url_for('admin.manage_reviews', username=current_user.username))
    
    page = request.args.get('page', 1, type=int)
    reviews = Review.query.order_by(Review.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/reviews.html', reviews=reviews)

@admin_bp.route("/<username>/admin/delete_review/<int:review_id>", methods=['POST'])
@login_required
@admin_required
def delete_review(username, review_id):
    if current_user.username != username:
        return redirect(url_for('admin.manage_reviews', username=current_user.username))
    
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    flash('Review has been deleted.')
    return redirect(url_for('admin.manage_reviews', username=username))
