import pytest
from unittest.mock import MagicMock

from services.admin_service import ban_user


@pytest.fixture(autouse=True)
def mock_db(monkeypatch):
    # Arrange
    mock_session = MagicMock()
    mock_db = MagicMock()
    mock_db.session = mock_session

    monkeypatch.setattr("services.admin_service.db", mock_db)

    return mock_db


@pytest.mark.parametrize(
    "username",
    [
        pytest.param("alice", id="happy-normal-username-alice"),
        pytest.param("bob_123", id="happy-username-with-underscore"),
        pytest.param("user.with.dots", id="happy-username-with-dots"),
        pytest.param("UPPERCASE", id="happy-uppercase-username"),
    ],
)
def test_ban_user_happy_path(mock_db, username):

    # Arrange
    user = MagicMock()
    user.username = username
    user.is_banned = False
    user.is_admin.return_value = False

    # Act
    success, message = ban_user(user)

    # Assert
    assert success is True
    assert user.is_banned is True
    mock_db.session.commit.assert_called_once()
    assert message == f"User {username} has been banned."
    user.is_admin.assert_called_once_with()




