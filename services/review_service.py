from models import Review, Book, db


def add_review(book_id, user_id, rating, comment):
    # Validate rating
    if rating is None:
        return False, 'Rating is required'
    
    if not isinstance(rating, int):
        return False, 'Rating must be a number'
    
    if rating < 1 or rating > 5:
        return False, 'Rating must be between 1 and 5'
    
    # Validate comment
    # if comment and len(comment.strip()) == 0:
    #     comment = None
    
    # if comment and len(comment) > 1000:
    #     return False, 'Comment cannot exceed 1000 characters'
    
    check_comment_result = check_comment(book_id, user_id, rating, comment)
    
    # Check if book exists
    book = db.session.get(Book, book_id)
    if not book:
        return False, 'Book not found'
    
    # Check for duplicate review
    existing_review = Review.query.filter_by(
        user_id=user_id,
        book_id=book_id
    ).first()
    
    if existing_review:
        return False, 'You have already reviewed this book'
    
    review = Review(
        rating=rating,
        comment=comment,
        user_id=user_id,
        book_id=book_id
    )
    db.session.add(review)
    db.session.commit()
    return True, review

def check_comment(book_id, user_id, rating, comment):
    # Validate comment
    if comment and len(comment.strip()) == 0:
        comment = None
    if comment and len(comment) > 1000:
        return False, 'Comment cannot exceed 1000 characters'
