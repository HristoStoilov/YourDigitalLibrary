from models import Review, db


def add_review(book_id, user_id, rating, comment):
    
    review = Review(
        rating=rating,
        comment=comment,
        user_id=user_id,
        book_id=book_id
    )
    db.session.add(review)
    db.session.commit()
    return review
