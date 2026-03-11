import pytest
from datetime import date
from unittest.mock import Mock, patch
from services.book_service import update_book

class TestUpdateBook:
    def test_update_book_all_fields(self):
        """Test update_book updates all fields and commits"""
        with patch('services.book_service.db.session') as mock_session:
            mock_book = Mock()
            mock_book.published_date = None

            result = update_book(
                mock_book,
                'New Title',
                'New Author',
                '0987654321',
                'New Description',
                '2023-01-15'
            )

            assert mock_book.title == 'New Title'
            assert mock_book.author == 'New Author'
            assert mock_book.isbn == '0987654321'
            assert mock_book.description == 'New Description'
            assert mock_book.published_date == date(2023, 1, 15)
            mock_session.commit.assert_called_once()
            assert result == mock_book