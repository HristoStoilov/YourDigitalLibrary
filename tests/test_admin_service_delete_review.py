import pytest
from unittest.mock import Mock, patch
from services.admin_service import delete_review

class TestDeleteReview:
    def test_delete_review_calls_delete(self):
        """Test that delete_review calls db.session.delete"""
        mock_review = Mock()
        
        with patch('services.admin_service.db.session') as mock_session:
            delete_review(mock_review)
            
            mock_session.delete.assert_called_once_with(mock_review)
    
    def test_delete_review_commits_transaction(self):
        """Test that delete_review commits the database transaction"""
        mock_review = Mock()
        
        with patch('services.admin_service.db.session') as mock_session:
            delete_review(mock_review)
            
            mock_session.commit.assert_called_once()
    
    def test_delete_review_with_different_review_objects(self):
        """Test delete_review with multiple different review objects"""
        mock_review1 = Mock(id=1)
        mock_review2 = Mock(id=2)
        
        with patch('services.admin_service.db.session') as mock_session:
            delete_review(mock_review1)
            delete_review(mock_review2)
            
            assert mock_session.delete.call_count == 2
            assert mock_session.commit.call_count == 2