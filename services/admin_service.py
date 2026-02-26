from datetime import datetime, timedelta
from sqlalchemy import func, or_
from models import User, Book, Review, db


def get_admin_dashboard_data():
    total_users = User.query.count()
    total_books = Book.query.count()
    total_reviews = Review.query.count()
    banned_users = User.query.filter_by(is_banned=True).count()

    seven_days_ago = datetime.utcnow() - timedelta(days=7)

    books_per_day = db.session.query(
        func.date(Book.created_at).label('date'),
        func.count(Book.id).label('count')
    ).filter(Book.created_at >= seven_days_ago).group_by(
        func.date(Book.created_at)
    ).order_by(func.date(Book.created_at)).all()

    reviews_per_day = db.session.query(
        func.date(Review.created_at).label('date'),
        func.count(Review.id).label('count')
    ).filter(Review.created_at >= seven_days_ago).group_by(
        func.date(Review.created_at)
    ).order_by(func.date(Review.created_at)).all()

    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    recent_books = Book.query.order_by(Book.created_at.desc()).limit(10).all()
    recent_reviews = Review.query.order_by(Review.created_at.desc()).limit(10).all()

    return {
        'total_users': total_users,
        'total_books': total_books,
        'total_reviews': total_reviews,
        'banned_users': banned_users,
        'books_per_day': books_per_day,
        'reviews_per_day': reviews_per_day,
        'recent_users': recent_users,
        'recent_books': recent_books,
        'recent_reviews': recent_reviews
    }


def get_users(page, search):
    query = User.query
    if search:
        query = query.filter(User.username.contains(search))
    return query.order_by(User.created_at.desc()).paginate(page=page, per_page=20)


def ban_user(user):
    if user.is_admin():
        return False, 'Cannot ban an admin user.'

    user.is_banned = True
    db.session.commit()
    return True, f'User {user.username} has been banned.'


def unban_user(user):
    user.is_banned = False
    db.session.commit()
    return True, f'User {user.username} has been unbanned.'


def get_reviews(page):
    return Review.query.order_by(Review.created_at.desc()).paginate(page=page, per_page=20)


def delete_review(review):
    db.session.delete(review)
    db.session.commit()


def get_books(page, search):
    query = Book.query
    if search:
        query = query.filter(
            or_(
                Book.title.contains(search),
                Book.author.contains(search)
            )
        )
    return query.order_by(Book.created_at.desc()).paginate(page=page, per_page=20)


def delete_book(book):
    book_title = book.title
    db.session.delete(book)
    db.session.commit()
    return book_title
