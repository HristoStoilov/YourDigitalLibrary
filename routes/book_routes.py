from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Book, Review, User, db
from datetime import datetime
from sqlalchemy.orm import joinedload

book_bp = Blueprint('book', __name__)

@book_bp.route("/books")
def books():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    author_filter = request.args.get('author', '')

    query = Book.query.options(joinedload(Book.submitter))

    if search:
        query = query.filter(Book.title.contains(search))
    if author_filter:
        query = query.filter(Book.author.contains(author_filter))

    books = query.paginate(page=page, per_page=10)
    return render_template("books.html", books=books, search=search, author_filter=author_filter)

@book_bp.route("/<username>/books")
@login_required
def user_books(username):
    if current_user.username != username:
        flash('You do not have permission to view this page.')
        return redirect(url_for('book.user_books', username=current_user.username))
    
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    author_filter = request.args.get('author', '')

    query = Book.query.options(joinedload(Book.submitter))

    if search:
        query = query.filter(Book.title.contains(search))
    if author_filter:
        query = query.filter(Book.author.contains(author_filter))

    books = query.paginate(page=page, per_page=10)
    return render_template("books.html", books=books, search=search, author_filter=author_filter)

@book_bp.route("/book/<int:book_id>")
def book_detail(book_id):
    book = Book.query.options(joinedload(Book.submitter)).get_or_404(book_id)
    reviews = Review.query.filter_by(book_id=book_id).options(joinedload(Review.author)).all()
    return render_template("book_detail.html", book=book, reviews=reviews)

@book_bp.route("/<username>/book/<int:book_id>")
@login_required
def user_book_detail(username, book_id):
    if current_user.username != username:
        flash('You do not have permission to view this page.')
        return redirect(url_for('book.user_book_detail', username=current_user.username, book_id=book_id))
    
    book = Book.query.options(joinedload(Book.submitter)).get_or_404(book_id)
    reviews = Review.query.filter_by(book_id=book_id).options(joinedload(Review.author)).all()
    return render_template("book_detail.html", book=book, reviews=reviews)

@book_bp.route("/<username>/add_book", methods=['GET', 'POST'])
@login_required
def add_book(username):
    if current_user.username != username:
        flash('You do not have permission to add books.')
        return redirect(url_for('book.user_books', username=current_user.username))
    
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
        return redirect(url_for('book.user_books', username=username))

    return render_template("add_book.html")

@book_bp.route("/<username>/edit_book/<int:book_id>", methods=['GET', 'POST'])
@login_required
def edit_book(username, book_id):
    if current_user.username != username:
        flash('You do not have permission to edit books.')
        return redirect(url_for('book.user_books', username=current_user.username))
    
    book = Book.query.get_or_404(book_id)
    if book.submitted_by != current_user.id:
        flash('You do not have permission to edit this book.')
        return redirect(url_for('book.user_book_detail', username=username, book_id=book.id))
    
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
        return redirect(url_for('book.user_book_detail', username=username, book_id=book.id))

    return render_template("edit_book.html", book=book)

@book_bp.route("/<username>/delete_book/<int:book_id>", methods=['POST'])
@login_required
def delete_book(username, book_id):
    if current_user.username != username:
        flash('You do not have permission to delete books.')
        return redirect(url_for('book.user_books', username=current_user.username))
    
    book = Book.query.get_or_404(book_id)
    if book.submitted_by != current_user.id:
        flash('You do not have permission to delete this book.')
        return redirect(url_for('book.user_book_detail', username=username, book_id=book.id))
    
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!')
    return redirect(url_for('book.user_books', username=username))
