from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Review, db

review_bp = Blueprint('review', __name__)

@review_bp.route("/add_review/<int:book_id>", methods=['POST'])
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
    return redirect(url_for('book.book_detail', book_id=book_id))
