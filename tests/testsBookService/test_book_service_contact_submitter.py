import pytest
from unittest.mock import Mock
from flask import Flask
from services.book_service import contact_submitter



class TestContactSubmitter:
    
    def test_contact_submitter_mail_not_configured(self):
        """Test contact_submitter raises when mail extension is missing"""
        app = Flask(__name__)

        with app.app_context():
            mock_book = Mock()
            mock_book.title = 'Test Book'
            mock_book.submitter = Mock(username='test_author', email='author@example.com')
            app.extensions = {}

            with pytest.raises(RuntimeError, match='Mail extension is not configured'):
                contact_submitter(
                    book=mock_book,
                    subject='Test',
                    message_body='Test',
                    sender_email='sender@example.com',
                    sender_username='test_sender'
                )

## TODO: Add more tests for contact_submitter that test its other functionalities
