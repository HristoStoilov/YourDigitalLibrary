from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_mail import Message
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

@book_bp.route("/user/books")
@login_required
def user_books():
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

@book_bp.route("/user/book/<int:book_id>")
@login_required
def user_book_detail(book_id):
    book = Book.query.options(joinedload(Book.submitter)).get_or_404(book_id)
    reviews = Review.query.filter_by(book_id=book_id).options(joinedload(Review.author)).all()
    return render_template("book_detail.html", book=book, reviews=reviews)

@book_bp.route("/user/add_book", methods=['GET', 'POST'])
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
        return redirect(url_for('book.user_books'))

    return render_template("add_book.html")

@book_bp.route("/user/edit_book/<int:book_id>", methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.submitted_by != current_user.id:
        flash('You do not have permission to edit this book.')
        return redirect(url_for('book.user_book_detail', book_id=book.id))
    
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
        return redirect(url_for('book.user_book_detail', book_id=book.id))

    return render_template("edit_book.html", book=book)

@book_bp.route("/user/delete_book/<int:book_id>", methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.submitted_by != current_user.id:
        flash('You do not have permission to delete this book.')
        return redirect(url_for('book.user_book_detail', book_id=book.id))
    
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!')
    return redirect(url_for('book.user_books'))

@book_bp.route("/book/<int:book_id>/contact", methods=['POST'])
@login_required
def contact_submitter(book_id):
    book = Book.query.options(joinedload(Book.submitter)).get_or_404(book_id)
    
    # Prevent users from contacting themselves
    if book.submitted_by == current_user.id:
        flash('You cannot send a message to yourself.')
        return redirect(url_for('book.book_detail', book_id=book_id))
    
    subject = request.form.get('subject')
    message_body = request.form.get('message')
    
    if not subject or not message_body:
        flash('Subject and message are required.')
        return redirect(url_for('book.book_detail', book_id=book_id))
    
    # Import mail here to avoid circular import
    from app import mail
    
    # Create email message
    msg = Message(
        subject=f"[Digital Library] {subject}",
        recipients=[book.submitter.email],
        reply_to=current_user.email
    )
    
    msg.body = f"""
Hello {book.submitter.username},

You have received a message from {current_user.username} regarding your book "{book.title}":

---
{message_body}
---

You can reply directly to this email to respond to {current_user.username} at: {current_user.email}

Best regards,
Digital Library Team
    """
    
    msg.html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #007bff;">Digital Library - New Message</h2>
                <p>Hello <strong>{book.submitter.username}</strong>,</p>
                <p>You have received a message from <strong>{current_user.username}</strong> regarding your book "<strong>{book.title}</strong>":</p>
                <div style="background: #f8f9fa; padding: 15px; border-left: 4px solid #007bff; margin: 20px 0;">
                    <p style="margin: 0; white-space: pre-wrap;">{message_body}</p>
                </div>
                <p>You can reply directly to this email to respond to {current_user.username} at: <a href="mailto:{current_user.email}">{current_user.email}</a></p>
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                <p style="color: #666; font-size: 0.9em;">Best regards,<br>Digital Library Team</p>
            </div>
        </body>
    </html>
    """
    
    try:
        mail.send(msg)
        flash(f'Your message has been sent to {book.submitter.username}!')
    except Exception as e:
        flash(f'Failed to send message. Please try again later or contact {book.submitter.email} directly.')
        print(f"Error sending email: {e}")
    
    return redirect(url_for('book.book_detail', book_id=book_id))
