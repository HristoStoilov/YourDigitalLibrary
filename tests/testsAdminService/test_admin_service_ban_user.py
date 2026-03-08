from unittest.mock import Mock, patch
from services.admin_service import ban_user


class TestBanUser:
    def test_ban_user_success(self):
        """Test that ban_user successfully bans a non-admin user"""
        mock_user = Mock()
        mock_user.username = "testuser"
        mock_user.is_banned = False
        mock_user.is_admin.return_value = False
        
        with patch('services.admin_service.db.session') as mock_db:
            success, message = ban_user(mock_user)
            
            assert success is True
            assert message == "User testuser has been banned."
            assert mock_user.is_banned is True
            mock_db.commit.assert_called_once()
    
    def test_ban_admin_user_fails(self):
        """Test that ban_user fails when trying to ban an admin user"""
        mock_admin_user = Mock()
        mock_admin_user.username = "adminuser"
        mock_admin_user.is_banned = False
        mock_admin_user.is_admin.return_value = True
        
        with patch('services.admin_service.db.session') as mock_db:
            success, message = ban_user(mock_admin_user)
            
            assert success is False
            assert message == "Cannot ban an admin user."
            assert mock_admin_user.is_banned is False
            mock_db.commit.assert_not_called()
    