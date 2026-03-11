from unittest.mock import Mock, patch
from services.auth_service import register_user


class TestRegisterUser:
    def test_register_user_success(self):
        """Test successful user registration"""
        with patch('services.auth_service.User') as mock_user_class, \
             patch('services.auth_service.db.session') as mock_session:
            mock_user_class.query.filter_by.return_value.first.return_value = None
            mock_user = Mock()
            mock_user_class.return_value = mock_user

            success, result = register_user('newuser', 'user@gmail.com', 'Password1')

            assert success is True
            assert result == mock_user
            mock_session.add.assert_called_once_with(mock_user)
            mock_session.commit.assert_called_once()

    def test_register_user_username_exists(self):
        """Test registration fails when username already exists"""
        with patch('services.auth_service.User') as mock_user_class:
            mock_user_class.query.filter_by.return_value.first.return_value = Mock()

            success, message = register_user('existing', 'user@gmail.com', 'Password1')

            assert success is False
            assert message == 'Username already exists'

    def test_register_user_email_exists(self):
        """Test registration fails when email already exists"""
        with patch('services.auth_service.User') as mock_user_class:
            mock_user_class.query.filter_by.side_effect = [
                Mock(first=Mock(return_value=None)),
                Mock(first=Mock(return_value=Mock()))
            ]

            success, message = register_user('newuser', 'existing@gmail.com', 'Password1')

            assert success is False
            assert message == 'Email already registered'

    def test_register_user_invalid_email(self):
        """Test registration fails for non-Gmail addresses"""
        with patch('services.auth_service.User') as mock_user_class, \
             patch('services.auth_service.db.session') as mock_session:
            mock_user_class.query.filter_by.return_value.first.return_value = None

            success, message = register_user('newuser', 'user@yahoo.com', 'Password1')

            assert success is False
            assert message == 'Only Gmail addresses (@gmail.com) are allowed'
            mock_session.add.assert_not_called()
            mock_session.commit.assert_not_called()

    def test_register_user_password_too_short(self):
        """Test registration fails when password is too short"""
        with patch('services.auth_service.User') as mock_user_class:
            mock_user_class.query.filter_by.return_value.first.return_value = None

            success, message = register_user('newuser', 'user@gmail.com', 'Pass1')

            assert success is False
            assert message == 'Password must be at least 6 characters long'

    def test_register_user_password_no_uppercase(self):
        """Test registration fails when password has no uppercase letter"""
        with patch('services.auth_service.User') as mock_user_class:
            mock_user_class.query.filter_by.return_value.first.return_value = None

            success, message = register_user('newuser', 'user@gmail.com', 'password1')

            assert success is False
            assert message == 'Password must contain at least one capital letter'

    def test_register_user_password_no_digit(self):
        """Test registration fails when password has no digit"""
        with patch('services.auth_service.User') as mock_user_class:
            mock_user_class.query.filter_by.return_value.first.return_value = None

            success, message = register_user('newuser', 'user@gmail.com', 'Password')

            assert success is False
            assert message == 'Password must contain at least one number'