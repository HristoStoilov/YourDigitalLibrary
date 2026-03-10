from unittest.mock import MagicMock, patch
from services.admin_service import get_users


class TestGetUsers:
    def test_get_users_without_search(self):
        """Test get_users without search parameter"""
        mock_user_query = MagicMock()
        mock_paginate = MagicMock()
        mock_user_query.order_by.return_value.paginate.return_value = mock_paginate
        
        with patch('services.admin_service.User') as mock_user:
            mock_user.query = mock_user_query
            result = get_users(page=1, search=None)
            
            mock_user_query.order_by.assert_called_once()
            mock_user_query.order_by.return_value.paginate.assert_called_once_with(page=1, per_page=20)
            assert result == mock_paginate

    def test_get_users_with_search(self):
        """Test get_users with search parameter"""
        mock_user_query = MagicMock()
        mock_filter = MagicMock()
        mock_user_query.filter.return_value = mock_filter
        mock_paginate = MagicMock()
        mock_filter.order_by.return_value.paginate.return_value = mock_paginate
        
        with patch('services.admin_service.User') as mock_user:
            mock_user.query = mock_user_query
            result = get_users(page=2, search="john")
            
            mock_user_query.filter.assert_called_once()
            mock_filter.order_by.assert_called_once()
            mock_filter.order_by.return_value.paginate.assert_called_once_with(page=2, per_page=20)
            assert result == mock_paginate
