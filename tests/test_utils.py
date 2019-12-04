import pytest

from application.utils import is_valid_isbn, resolve_book_details


@pytest.fixture
def mock(mocker):
    mock = mocker.Mock()
    mocker.patch('application.utils.requests', mock)

    mock.get.return_value.status_code = 200
    mock.get.return_value.json.return_value = {
        "totalItems": 1,
        "items": [
            {
                "volumeInfo": {
                    "title": "Mocked book",
                    "authors": ["J.K. Rowling"],
                    "ISBN": "9783161484100"
                }
            }
        ]
    }

    return mock


@pytest.mark.usefixtures("mock")
def test_correct_book_details_are_resolved():
    details = resolve_book_details("9783161484100")
    assert details["author"] == "J.K. Rowling"
    assert details["title"] == "Mocked book"
    assert details["ISBN"] == "9783161484100"


def test_ISBN_validation_works():
    assert is_valid_isbn("9783161484100")


def test_ISBN_validation_with_invalid_value():
    assert not is_valid_isbn("abcdefghij")
    assert not is_valid_isbn("123456")


def test_valueError_is_raided_with_wrong_isbn():
    with pytest.raises(ValueError):
        resolve_book_details("97801323508")
