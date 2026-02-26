from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from services.review_service import add_review as add_review_service

review_bp = Blueprint('review', __name__)

@review_bp.route("/user/add_review/<int:book_id>", methods=['POST'])
@login_required
def user_add_review(book_id):
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment')

    add_review_service(book_id=book_id, user_id=current_user.id, rating=rating, comment=comment)

    flash('Review added successfully!')
    return redirect(url_for('book.user_book_detail', book_id=book_id))
