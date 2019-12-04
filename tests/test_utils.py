import pytest
from application import utils


def test_correct_book_details_are_resolved():
    ISBN = "9780132350884"
    details = utils.resolve_book_details(ISBN)
    assert details["author"] == "Robert C. Martin"
    assert details["title"] == "Clean Code"
    assert details["ISBN"] == ISBN


def test_ISBN_validation_works():
        ISBN = "97801323508"
        assert utils.is_valid_isbn(ISBN) is False
        ISBN = "abcdefghij"
        assert utils.is_valid_isbn(ISBN) is False


def test_valueError_is_raided_with_wrong_isbn():
    with pytest.raises(ValueError):
        ISBN = "97801323508"
        details = utils.resolve_book_details(ISBN)


def test_no_book_details_are_returned_with_wrong_isbn():
    ISBN = "97801323508"
    assert utils._get_book_details(ISBN) is None
