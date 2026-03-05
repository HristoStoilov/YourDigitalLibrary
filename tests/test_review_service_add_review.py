import pytest
from services import review_service
from services.review_service import add_review


# ----- Dummies and test doubles -----


class DummySession:
    def __init__(self):
        self._book_store = {}  # book_id -> DummyBook
        self.added = []
        self.committed = 0

    # Simulate SQLAlchemy Session.get(Model, pk)
    def get(self, model, pk):
        # Only Book is used with get in this service
        if model is DummyBook:
            return self._book_store.get(pk)
        return None

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        self.committed += 1


class DummyQuery:
    def __init__(self, existing_review=None):
        self._existing_review = existing_review
        self._filter_args = None
        self._filter_kwargs = None

    def filter_by(self, *args, **kwargs):
        self._filter_args = args
        self._filter_kwargs = kwargs
        return self

    def first(self):
        return self._existing_review


class DummyReview:
    # Mimic Review model enough for the service
    query = DummyQuery()

    def __init__(self, rating, comment, user_id, book_id):
        self.rating = rating
        self.comment = comment
        self.user_id = user_id
        self.book_id = book_id


class DummyBook:
    def __init__(self, id_):
        self.id = id_


class DummyDB:
    def __init__(self, session):
        self.session = session


@pytest.fixture(autouse=True)
def setup_review_env(monkeypatch):
    """
    Auto-used fixture that replaces Review, Book, and db in review_service
    with controllable test doubles.
    """

    # Arrange
    session = DummySession()
    dummy_db = DummyDB(session=session)

    # Patch db, Book, and Review inside the review_service module
    monkeypatch.setattr(review_service, "db", dummy_db)
    monkeypatch.setattr(review_service, "Book", DummyBook)
    monkeypatch.setattr(review_service, "Review", DummyReview)

    return session


# ----- Happy path tests -----


@pytest.mark.parametrize(
    "book_id,user_id,rating,comment",
    [
        pytest.param(
            1,
            10,
            5,
            "Amazing book, highly recommended!",
            id="happy-max-rating_with_comment",
        ),
        pytest.param(
            2,
            20,
            3,
            "It was okay, some parts were slow.",
            id="happy-mid-rating_with_comment",
        ),
        pytest.param(
            3,
            30,
            1,
            "Did not enjoy this book.",
            id="happy-min-rating_with_comment",
        ),
        pytest.param(
            4,
            40,
            4,
            None,
            id="happy-rating_no_comment",
        ),
        pytest.param(
            5,
            50,
            2,
            "",
            id="happy-rating_empty_comment_treated_as_none",
        ),
        pytest.param(
            6,
            60,
            5,
            "   Great book with leading/trailing spaces   ",
            id="happy-rating_comment_with_extra_spaces",
        ),
    ],
)
def test_add_review_happy_paths(setup_review_env, book_id, user_id, rating, comment):
    session = setup_review_env

    # Arrange
    session._book_store[book_id] = DummyBook(book_id)
    DummyReview.query = DummyQuery(existing_review=None)

    # Act
    success, result = review_service.add_review(
        book_id=book_id, user_id=user_id, rating=rating, comment=comment
    )

    # Assert
    assert success is True
    assert isinstance(result, DummyReview)
    assert result.rating == rating
    # Comment normalization: empty/whitespace-only comments become None
    if comment and len(comment.strip()) == 0:
        assert result.comment is None
    elif comment is None:
        assert result.comment is None
    else:
        # Spaces are not stripped by the function; only zero-length after strip becomes None
        assert result.comment == comment
    assert result.user_id == user_id
    assert result.book_id == book_id

    # DB interactions
    assert session.added == [result]
    assert session.committed == 1


@pytest.mark.parametrize(
    "comment,expected_message,case_id",
    [
        pytest.param(
            "a" * 1001,
            "Comment cannot exceed 1000 characters",
            "error-comment-too-long",
            id="error-comment-too-long",
        ),
    ],
)
def test_add_review_error_comment_too_long(
    setup_review_env, comment, expected_message, case_id
):
    session = setup_review_env

    # Arrange
    book_id = 2
    user_id = 2
    rating = 4
    session._book_store[book_id] = DummyBook(book_id)
    DummyReview.query = DummyQuery(existing_review=None)

    # Act
    success, message = review_service.add_review(
        book_id=book_id, user_id=user_id, rating=rating, comment=comment
    )

    # Assert
    assert success is False
    assert message == expected_message
    # No DB write operations should have occurred
    assert session.added == []
    assert session.committed == 0

@pytest.mark.parametrize(
    "existing_comment,existing_rating",
    [
        pytest.param(
            "Already reviewed this.",
            4,
            id="error-duplicate-review-existing-with-comment",
        ),
        pytest.param(
            None,
            5,
            id="error-duplicate-review-existing-without-comment",
        ),
    ],
)
def test_add_review_error_duplicate_review(
    setup_review_env, existing_comment, existing_rating
):
    session = setup_review_env

    # Arrange
    book_id = 10
    user_id = 20
    rating = 5
    comment = "My new review"
    session._book_store[book_id] = DummyBook(book_id)

    existing_review = DummyReview(
        rating=existing_rating,
        comment=existing_comment,
        user_id=user_id,
        book_id=book_id,
    )
    DummyReview.query = DummyQuery(existing_review=existing_review)

    # Act
    success, message = review_service.add_review(
        book_id=book_id, user_id=user_id, rating=rating, comment=comment
    )

    # Assert
    assert success is False
    assert message == "You have already reviewed this book"
    assert session.added == []
    assert session.committed == 0


