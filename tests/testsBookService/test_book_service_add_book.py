from datetime import date
from unittest.mock import Mock, patch
from services.book_service import add_book


class TestAddBook:
    def test_add_book_with_valid_date(self):
        """Test add_book parses valid date and persists book"""
        with patch('services.book_service.Book') as mock_book_class, \
             patch('services.book_service.db.session') as mock_session:
            mock_book_instance = Mock()
            mock_book_class.return_value = mock_book_instance

            result = add_book('Test Title', 'Test Author', '123-456', 'Description', '2023-01-15', 1)

            mock_book_class.assert_called_once_with(
                title='Test Title',
                author='Test Author',
                isbn='123-456',
                description='Description',
                published_date=date(2023, 1, 15),
                submitted_by=1
            )
            mock_session.add.assert_called_once_with(mock_book_instance)
            mock_session.commit.assert_called_once()
            assert result == mock_book_instance

    def test_add_book_with_none_date(self):
        """Test add_book keeps published_date None when input date is None"""
        with patch('services.book_service.Book') as mock_book_class, \
             patch('services.book_service.db.session') as mock_session:
            mock_book_instance = Mock()
            mock_book_class.return_value = mock_book_instance

            result = add_book('Test Title', 'Test Author', '123-456', 'Description', None, 1)

            mock_book_class.assert_called_once_with(
                title='Test Title',
                author='Test Author',
                isbn='123-456',
                description='Description',
                published_date=None,
                submitted_by=1
            )
            mock_session.add.assert_called_once_with(mock_book_instance)
            mock_session.commit.assert_called_once()
            assert result == mock_book_instance

    def test_add_book_with_empty_date_string(self):
        """Test add_book keeps published_date None for whitespace-only date string"""
        with patch('services.book_service.Book') as mock_book_class, \
             patch('services.book_service.db.session') as mock_session:
            mock_book_instance = Mock()
            mock_book_class.return_value = mock_book_instance

            result = add_book('Test Title', 'Test Author', '123-456', 'Description', '   ', 1)

            mock_book_class.assert_called_once_with(
                title='Test Title',
                author='Test Author',
                isbn='123-456',
                description='Description',
                published_date=None,
                submitted_by=1
            )
            mock_session.add.assert_called_once_with(mock_book_instance)
            mock_session.commit.assert_called_once()
            assert result == mock_book_instance
