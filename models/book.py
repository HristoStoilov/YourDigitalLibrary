from datetime import datetime
from models import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    isbn = db.Column(db.String(13), unique=True)
    description = db.Column(db.Text)
    published_date = db.Column(db.Date)
    cover_image = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    submitted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    reviews = db.relationship('Review', backref='book', lazy=True, cascade='all, delete-orphan')
    submitter = db.relationship('User', backref='books_submitted', lazy=True)
    
    def __repr__(self):
        return f'<Book {self.title}>'
