from unittest.mock import Mock, patch
from services.admin_service import unban_user


class TestUnbanUser:
    def test_unban_user_success(self):
        """Test that unban_user successfully unbans a banned user"""
        mock_user = Mock()
        mock_user.username = 'testuser'
        mock_user.is_banned = True
        
        with patch('services.admin_service.db.session') as mock_db_session:
            success, message = unban_user(mock_user)
            
            assert success is True
            assert mock_user.is_banned is False
            assert message == 'User testuser has been unbanned.'
            mock_db_session.commit.assert_called_once()
    

#    def test_unban_user_commits_changes(self):
#        """Test that unban_user commits the database transaction"""
#        mock_user = Mock()
#        mock_user.username = 'testuser'
#        mock_user.is_banned = True
#        
#        with patch('services.admin_service.db.session') as mock_db_session:
#            unban_user(mock_user)
#            
#            mock_db_session.commit.assert_called_once()
    