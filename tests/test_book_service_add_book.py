import pytest
from datetime import date
from services import book_service
from services.book_service import add_book

# Dummy session to capture DB interactions
class DummySession:
    def __init__(self):
        self.added = []
        self.committed = 0

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        self.committed += 1


# Dummy DB wrapper
class DummyDB:
    def __init__(self):
        self.session = DummySession()


# Dummy Book model to capture constructor arguments
class DummyBook:
    def __init__(self, title, author, isbn, description, published_date, submitted_by):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.description = description
        self.published_date = published_date
        self.submitted_by = submitted_by


@pytest.fixture(autouse=True)
def mock_models(monkeypatch):
    """
    Auto-used fixture to replace the real Book and db objects in book_service
    with simple in-memory doubles so we can assert behavior without hitting
    any real database.
    """

    # Arrange
    dummy_db = DummyDB()

    # Bind DummyDB as the db used inside book_service
    monkeypatch.setattr(book_service, "db", dummy_db)

    # Book factory that produces DummyBook instances
    def book_factory(title, author, isbn, description, published_date, submitted_by):
        return DummyBook(
            title=title,
            author=author,
            isbn=isbn,
            description=description,
            published_date=published_date,
            submitted_by=submitted_by,
        )

    monkeypatch.setattr(book_service, "Book", book_factory)

    return dummy_db


@pytest.mark.parametrize(
    "title,author,isbn,description,published_date_str,submitted_by,expected_date",
    [
        pytest.param(
            "The Pragmatic Programmer",
            "Andrew Hunt",
            "978-0201616224",
            "Classic software engineering book.",
            "1999-10-30",
            "user1",
            date(1999, 10, 30),
            id="happy-classic-software-book",
        ),
        pytest.param(
            "Clean Code",
            "Robert C. Martin",
            "978-0132350884",
            "A Handbook of Agile Software Craftsmanship.",
            "2008-08-01",
            "user2",
            date(2008, 8, 1),
            id="happy-clean-code-agile",
        ),
        pytest.param(
            "Deep Learning",
            "Ian Goodfellow",
            "978-0262035613",
            "Deep learning reference.",
            "2016-11-18",
            "ml_researcher",
            date(2016, 11, 18),
            id="happy-deep-learning-reference",
        ),
        pytest.param(
            "Python Testing with pytest",
            "Brian Okken",
            "978-1680502404",
            "Guide to testing in Python.",
            "2017-09-01",
            "test_engineer",
            date(2017, 9, 1),
            id="happy-pytest-testing-guide",
        ),
    ],
)
def test_add_book_happy_path(
    mock_models,
    title,
    author,
    isbn,
    description,
    published_date_str,
    submitted_by,
    expected_date,
):

    # Act
    book = book_service.add_book(
        title=title,
        author=author,
        isbn=isbn,
        description=description,
        published_date_str=published_date_str,
        submitted_by=submitted_by,
    )

    # Assert
    assert isinstance(book, DummyBook)
    assert book.title == title
    assert book.author == author
    assert book.isbn == isbn
    assert book.description == description
    assert book.published_date == expected_date
    assert book.submitted_by == submitted_by

    # DB interactions
    assert mock_models.session.added == [book]
    assert mock_models.session.committed == 1








