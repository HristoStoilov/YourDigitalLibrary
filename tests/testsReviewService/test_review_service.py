import pytest
from services.review_service import check_comment

class TestCheckComment:
    def test_check_comment_with_valid_comment(self):
        result = check_comment(1, 1, 5, "Great book!")
        assert result is None
    
    def test_check_comment_with_empty_string(self):
        result = check_comment(1, 1, 5, "")
        assert result is None
    
    def test_check_comment_with_whitespace_only(self):
        result = check_comment(1, 1, 5, "   ")
        assert result is None
    
    def test_check_comment_with_none(self):
        result = check_comment(1, 1, 5, None)
        assert result is None
    
    def test_check_comment_exceeds_max_length(self):
        long_comment = "a" * 1001
        result = check_comment(1, 1, 5, long_comment)
        assert result == (False, 'Comment cannot exceed 1000 characters')
    
    def test_check_comment_at_max_length(self):
        max_comment = "a" * 1000
        result = check_comment(1, 1, 5, max_comment)
        assert result is None
    
    def test_check_comment_with_mixed_whitespace(self):
        result = check_comment(1, 1, 5, "\t\n ")
        assert result is None