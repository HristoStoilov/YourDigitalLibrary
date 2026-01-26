from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Book, Review, db
from datetime import datetime

book_bp = Blueprint('book', __name__)

@book_bp.route("/books")
def books():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    author_filter = request.args.get('author', '')

    query = Book.query

    if search:
        query = query.filter(Book.title.contains(search))
    if author_filter:
        query = query.filter(Book.author.contains(author_filter))

    books = query.paginate(page=page, per_page=10)
    return render_template("books.html", books=books, search=search, author_filter=author_filter)

@book_bp.route("/book/<int:book_id>")
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    reviews = Review.query.filter_by(book_id=book_id).all()
    return render_template("book_detail.html", book=book, reviews=reviews)

@book_bp.route("/add_book", methods=['GET', 'POST'])
@login_required
def add_book():
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
        return redirect(url_for('book.books'))

    return render_template("add_book.html")

@book_bp.route("/edit_book/<int:book_id>", methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.submitted_by != current_user.id:
        flash('You do not have permission to edit this book.')
        return redirect(url_for('book.book_detail', book_id=book.id))
    
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
        return redirect(url_for('book.book_detail', book_id=book.id))

    return render_template("edit_book.html", book=book)

@book_bp.route("/delete_book/<int:book_id>", methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.submitted_by != current_user.id:
        flash('You do not have permission to delete this book.')
        return redirect(url_for('book.book_detail', book_id=book.id))
    
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!')
    return redirect(url_for('book.books'))
