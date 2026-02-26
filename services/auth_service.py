from models import User, Book, Review, db
from sqlalchemy.orm import joinedload


def register_user(username, email, password):
    if User.query.filter_by(username=username).first():
        return False, 'Username already exists'

    if User.query.filter_by(email=email).first():
        return False, 'Email already registered'

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return True, user


def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None


def get_user_dashboard_data(user_id):
    
    total_books_added = Book.query.filter_by(submitted_by=user_id).count()
    total_reviews_written = Review.query.filter_by(user_id=user_id).count()
    recent_books = Book.query.filter_by(submitted_by=user_id).order_by(Book.created_at.desc()).limit(5).all()
    recent_reviews = Review.query.filter_by(user_id=user_id).options(joinedload(Review.book)).order_by(Review.created_at.desc()).limit(5).all()

    return {
        'total_books_added': total_books_added,
        'total_reviews_written': total_reviews_written,
        'recent_books': recent_books,
        'recent_reviews': recent_reviews
    }


def change_user_password(user, current_password, new_password, confirm_password):
    
    if not user.check_password(current_password):
        return False, 'Current password is incorrect.'

    if new_password != confirm_password:
        return False, 'New passwords do not match.'

    if len(new_password) < 6:
        return False, 'New password must be at least 6 characters long.'

    user.set_password(new_password)
    db.session.commit()
    return True, 'Password changed successfully!'
