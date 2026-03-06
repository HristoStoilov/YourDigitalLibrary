import pytest
from unittest.mock import Mock, patch, MagicMock
from services.admin_service import delete_book

class TestDeleteBook:
    def test_delete_book_returns_title(self):
        """Test that delete_book returns the book title"""
        mock_book = Mock()
        mock_book.title = "Test Book Title"
        
        with patch('services.admin_service.db.session') as mock_session:
            result = delete_book(mock_book)
            
            assert result == "Test Book Title"
    
    def test_delete_book_calls_delete(self):
        """Test that delete_book calls db.session.delete"""
        mock_book = Mock()
        mock_book.title = "Test Book"
        
        with patch('services.admin_service.db.session') as mock_session:
            delete_book(mock_book)
            
            mock_session.delete.assert_called_once_with(mock_book)
    
    def test_delete_book_commits_transaction(self):
        """Test that delete_book commits the database transaction"""
        mock_book = Mock()
        mock_book.title = "Test Book"
        
        with patch('services.admin_service.db.session') as mock_session:
            delete_book(mock_book)
            
            mock_session.commit.assert_called_once()
    
    def test_delete_book_with_special_characters(self):
        """Test delete_book with special characters in title"""
        mock_book = Mock()
        mock_book.title = "Test: Book's \"Special\" Title!"
        
        with patch('services.admin_service.db.session'):
            result = delete_book(mock_book)
            
            assert result == "Test: Book's \"Special\" Title!"