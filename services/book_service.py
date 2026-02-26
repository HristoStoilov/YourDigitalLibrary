from datetime import datetime
from flask import current_app
from flask_mail import Message
from sqlalchemy.orm import joinedload
from models import Book, Review, db


def get_books(page, search, author_filter):
   
    query = Book.query.options(joinedload(Book.submitter))

    if search:
        query = query.filter(Book.title.contains(search))
    if author_filter:
        query = query.filter(Book.author.contains(author_filter))

    return query.paginate(page=page, per_page=10)


def get_book_detail(book_id):
    
    book = Book.query.options(joinedload(Book.submitter)).get_or_404(book_id)
    reviews = Review.query.filter_by(book_id=book_id).options(joinedload(Review.author)).all()
    return book, reviews


def add_book(title, author, isbn, description, published_date_str, submitted_by):
   
    published_date = None
    if published_date_str:
        published_date = datetime.strptime(published_date_str, '%Y-%m-%d').date()

    book = Book(
        title=title,
        author=author,
        isbn=isbn,
        description=description,
        published_date=published_date,
        submitted_by=submitted_by
    )
    db.session.add(book)
    db.session.commit()
    return book


def update_book(book, title, author, isbn, description, published_date_str):
   
    book.title = title
    book.author = author
    book.isbn = isbn
    book.description = description

    if published_date_str:
        book.published_date = datetime.strptime(published_date_str, '%Y-%m-%d').date()

    db.session.commit()
    return book


def delete_book(book):
    db.session.delete(book)
    db.session.commit()


def contact_submitter(book, subject, message_body, sender_email, sender_username):
   
    mail = current_app.extensions.get('mail')
    if not mail:
        raise RuntimeError('Mail extension is not configured.')

    msg = Message(
        subject=f"[Digital Library] {subject}",
        recipients=[book.submitter.email],
        reply_to=sender_email
    )

    msg.body = f"""
Hello {book.submitter.username},

You have received a message from {sender_username} regarding your book "{book.title}":

---
{message_body}
---

You can reply directly to this email to respond to {sender_username} at: {sender_email}

Best regards,
Digital Library Team
    """

    msg.html = f"""
    <html>
        <body style=\"font-family: Arial, sans-serif; line-height: 1.6; color: #333;\">
            <div style=\"max-width: 600px; margin: 0 auto; padding: 20px;\">
                <h2 style=\"color: #007bff;\">Digital Library - New Message</h2>
                <p>Hello <strong>{book.submitter.username}</strong>,</p>
                <p>You have received a message from <strong>{sender_username}</strong> regarding your book "<strong>{book.title}</strong>":</p>
                <div style=\"background: #f8f9fa; padding: 15px; border-left: 4px solid #007bff; margin: 20px 0;\">
                    <p style=\"margin: 0; white-space: pre-wrap;\">{message_body}</p>
                </div>
                <p>You can reply directly to this email to respond to {sender_username} at: <a href=\"mailto:{sender_email}\">{sender_email}</a></p>
                <hr style=\"border: none; border-top: 1px solid #ddd; margin: 20px 0;\">
                <p style=\"color: #666; font-size: 0.9em;\">Best regards,<br>Digital Library Team</p>
            </div>
        </body>
    </html>
    """

    mail.send(msg)
