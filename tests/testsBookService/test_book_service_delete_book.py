from unittest.mock import Mock, patch
from services.book_service import delete_book


class TestDeleteBook:
    def test_delete_book_calls_delete(self):
        """Test delete_book calls db.session.delete with the book"""
        with patch('services.book_service.db.session') as mock_session:
            mock_book = Mock(id=1, title='Test Book')

            delete_book(mock_book)

            mock_session.delete.assert_called_once_with(mock_book)

    def test_delete_book_commits_session(self):
        """Test delete_book commits the session"""
        with patch('services.book_service.db.session') as mock_session:
            mock_book = Mock(id=1, title='Test Book')

            delete_book(mock_book)

            mock_session.commit.assert_called_once()

