"""
Admin Controller
Handles administrative routes for managing users, books, and reviews.
Includes admin authorization decorator.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import User, Book, Review
from services.admin_service import (
    get_admin_dashboard_data,
    get_users,
    ban_user as ban_user_service,
    unban_user as unban_user_service,
    get_reviews,
    delete_review as delete_review_service,
    get_books as get_books_service,
    delete_book as delete_book_service
)
from functools import wraps

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    """Decorator to require admin privileges for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You do not have permission to access this page.')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route("/user/admin/dashboard")
@login_required
@admin_required
def admin_dashboard():
    """Display admin dashboard with statistics"""
    stats = get_admin_dashboard_data()

    return render_template('admin/dashboard.html',
                         total_users=stats['total_users'],
                         total_books=stats['total_books'],
                         total_reviews=stats['total_reviews'],
                         banned_users=stats['banned_users'],
                         books_per_day=stats['books_per_day'],
                         reviews_per_day=stats['reviews_per_day'],
                         recent_users=stats['recent_users'],
                         recent_books=stats['recent_books'],
                         recent_reviews=stats['recent_reviews'])


@admin_bp.route("/user/admin/users")
@login_required
@admin_required
def manage_users():
    """Display user management page"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')

    users = get_users(page, search)
    return render_template('admin/users.html', users=users, search=search)


@admin_bp.route("/user/admin/ban_user/<int:user_id>", methods=['POST'])
@login_required
@admin_required
def ban_user(user_id):
    """Ban a user"""
    user = User.query.get_or_404(user_id)

    success, message = ban_user_service(user)
    if not success:
        flash(message)
        return redirect(url_for('admin.manage_users'))

    flash(message)
    return redirect(url_for('admin.manage_users'))


@admin_bp.route("/user/admin/unban_user/<int:user_id>", methods=['POST'])
@login_required
@admin_required
def unban_user(user_id):
    """Unban a user"""
    user = User.query.get_or_404(user_id)

    success, message = unban_user_service(user)
    flash(message)
    return redirect(url_for('admin.manage_users'))


@admin_bp.route("/user/admin/reviews")
@login_required
@admin_required
def manage_reviews():
    """Display review management page"""
    page = request.args.get('page', 1, type=int)
    reviews = get_reviews(page)
    return render_template('admin/reviews.html', reviews=reviews)


@admin_bp.route("/user/admin/delete_review/<int:review_id>", methods=['POST'])
@login_required
@admin_required
def delete_review(review_id):
    """Delete a review"""
    review = Review.query.get_or_404(review_id)
    delete_review_service(review)
    flash('Review has been deleted.')
    return redirect(url_for('admin.manage_reviews'))


@admin_bp.route("/user/admin/books")
@login_required
@admin_required
def manage_books():
    """Display book management page"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')

    books = get_books_service(page, search)
    return render_template('admin/books.html', books=books, search=search)


@admin_bp.route("/user/admin/delete_book/<int:book_id>", methods=['POST'])
@login_required
@admin_required
def delete_book(book_id):
    """Delete a book"""
    book = Book.query.get_or_404(book_id)
    book_title = delete_book_service(book)
    flash(f'Book "{book_title}" has been deleted.')
    return redirect(url_for('admin.manage_books'))
