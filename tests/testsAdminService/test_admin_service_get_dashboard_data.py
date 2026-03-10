from unittest.mock import MagicMock, patch
from services.admin_service import get_admin_dashboard_data

class TestGetAdminDashboardData:
    def _setup_common_mocks(self, mock_user, mock_book, mock_review, mock_db_session):
        mock_book_created_at = MagicMock()
        mock_book_created_at.__ge__.return_value = MagicMock()
        mock_book_created_at.desc.return_value = MagicMock()
        mock_book.created_at = mock_book_created_at

        mock_review_created_at = MagicMock()
        mock_review_created_at.__ge__.return_value = MagicMock()
        mock_review_created_at.desc.return_value = MagicMock()
        mock_review.created_at = mock_review_created_at

        mock_user_created_at = MagicMock()
        mock_user_created_at.desc.return_value = MagicMock()
        mock_user.created_at = mock_user_created_at

        mock_user_query = mock_user.query
        mock_book_query = mock_book.query
        mock_review_query = mock_review.query

        mock_db_session.query.return_value.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = []
        mock_user_query.order_by.return_value.limit.return_value.all.return_value = []
        mock_book_query.order_by.return_value.limit.return_value.all.return_value = []
        mock_review_query.order_by.return_value.limit.return_value.all.return_value = []

    def test_get_admin_dashboard_data_returns_all_keys(self):
        with patch('services.admin_service.User') as mock_user, \
             patch('services.admin_service.Book') as mock_book, \
             patch('services.admin_service.Review') as mock_review, \
             patch('services.admin_service.db.session') as mock_db_session:
            mock_user_query = mock_user.query
            mock_book_query = mock_book.query
            mock_review_query = mock_review.query

            mock_user_query.count.return_value = 10
            mock_book_query.count.return_value = 5
            mock_review_query.count.return_value = 15
            mock_user_query.filter_by.return_value.count.return_value = 2
            self._setup_common_mocks(mock_user, mock_book, mock_review, mock_db_session)

            result = get_admin_dashboard_data()

            assert 'total_users' in result
            assert 'total_books' in result
            assert 'total_reviews' in result
            assert 'banned_users' in result
            assert 'books_per_day' in result
            assert 'reviews_per_day' in result
            assert 'recent_users' in result
            assert 'recent_books' in result
            assert 'recent_reviews' in result

    def test_get_admin_dashboard_data_correct_counts(self):
        with patch('services.admin_service.User') as mock_user, \
             patch('services.admin_service.Book') as mock_book, \
             patch('services.admin_service.Review') as mock_review, \
             patch('services.admin_service.db.session') as mock_db_session:
            mock_user_query = mock_user.query
            mock_book_query = mock_book.query
            mock_review_query = mock_review.query

            mock_user_query.count.return_value = 25
            mock_book_query.count.return_value = 100
            mock_review_query.count.return_value = 50
            mock_user_query.filter_by.return_value.count.return_value = 3
            self._setup_common_mocks(mock_user, mock_book, mock_review, mock_db_session)

            result = get_admin_dashboard_data()

            assert result['total_users'] == 25
            assert result['total_books'] == 100
            assert result['total_reviews'] == 50
            assert result['banned_users'] == 3