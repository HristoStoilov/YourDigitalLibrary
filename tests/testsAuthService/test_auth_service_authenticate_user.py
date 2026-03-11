from unittest.mock import Mock, patch
from services.auth_service import authenticate_user


class TestAuthenticateUser:
    def test_authenticate_user_success(self):
        """Test authenticate_user returns user for valid credentials"""
        with patch('services.auth_service.User') as mock_user_class:
            mock_user = Mock()
            mock_user.check_password.return_value = True
            mock_user_class.query.filter_by.return_value.first.return_value = mock_user

            result = authenticate_user('testuser', 'password123')

            assert result == mock_user
            mock_user_class.query.filter_by.assert_called_once_with(username='testuser')
            mock_user.check_password.assert_called_once_with('password123')


    def test_authenticate_user_invalid_password(self):
        """Test authenticate_user returns None for wrong password"""
        with patch('services.auth_service.User') as mock_user_class:
            mock_user = Mock()
            mock_user.check_password.return_value = False
            mock_user_class.query.filter_by.return_value.first.return_value = mock_user

            result = authenticate_user('testuser', 'wrongpassword')

            assert result is None
            mock_user_class.query.filter_by.assert_called_once_with(username='testuser')
            mock_user.check_password.assert_called_once_with('wrongpassword')


    def test_authenticate_user_nonexistent_user(self):
        """Test authenticate_user returns None when user does not exist"""
        with patch('services.auth_service.User') as mock_user_class:
            mock_user_class.query.filter_by.return_value.first.return_value = None

            result = authenticate_user('nonexistent', 'password123')

            assert result is None
            mock_user_class.query.filter_by.assert_called_once_with(username='nonexistent')


    def test_authenticate_user_user_exists_check_password_called(self):
        """Test authenticate_user calls check_password when user exists"""
        with patch('services.auth_service.User') as mock_user_class:
            mock_user = Mock()
            mock_user.check_password.return_value = True
            mock_user_class.query.filter_by.return_value.first.return_value = mock_user

            authenticate_user('testuser', 'password123')

            mock_user.check_password.assert_called_once_with('password123')