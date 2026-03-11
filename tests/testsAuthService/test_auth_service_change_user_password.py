from unittest.mock import Mock, patch
from services.auth_service import change_user_password


class TestChangeUserPassword:
    def test_incorrect_current_password(self):
        """Test change_user_password fails when current password is incorrect"""
        user = Mock()
        user.check_password.return_value = False

        success, message = change_user_password(user, 'wrong', 'NewPass1', 'NewPass1')

        assert success is False
        assert message == 'Current password is incorrect.'

    def test_passwords_do_not_match(self):
        """Test change_user_password fails when new passwords do not match"""
        user = Mock()
        user.check_password.return_value = True

        success, message = change_user_password(user, 'Current1', 'NewPass1', 'NewPass2')

        assert success is False
        assert message == 'New passwords do not match.'

    def test_new_password_too_short(self):
        """Test change_user_password fails when new password is too short"""
        user = Mock()
        user.check_password.return_value = True

        success, message = change_user_password(user, 'Current1', 'Pass', 'Pass')

        assert success is False
        assert message == 'New password must be at least 6 characters long.'

    def test_password_changed_successfully(self):
        """Test change_user_password updates password and commits on success"""
        with patch('services.auth_service.db.session.commit') as mock_commit:
            user = Mock()
            user.check_password.return_value = True

            success, message = change_user_password(user, 'Current1', 'NewPass1', 'NewPass1')

            assert success is True
            assert message == 'Password changed successfully!'
            user.set_password.assert_called_once_with('NewPass1')
            mock_commit.assert_called_once()