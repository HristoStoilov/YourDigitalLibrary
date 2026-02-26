"""
Database Models Package
This package defines all database models for the application.
Models represent the data layer in the MVC architecture.
"""
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

# Import all models to make them available when importing from models package
from models.user import User
from models.book import Book
from models.review import Review

# Export all models and db instance
__all__ = ['db', 'User', 'Book', 'Review']
