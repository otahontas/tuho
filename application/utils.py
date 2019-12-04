import re

import requests


API_URL = 'https://www.googleapis.com/books/v1/volumes'


def resolve_book_details(ISBN):
    """
    Return dict containing author and book title based on ISBN.

    Args:
        ISBN: Book ISBN-number as string without hyphens, containing 10 or 13 numbers
    Returns:
        Dict containing keys: author, title and ISBN or None if book not found
    """

    if not is_valid_isbn(ISBN):
        raise ValueError(f"Invalid ISBN {ISBN}")

    data = _get_book_details(ISBN)
    if not data:
        return {}

    book = data["items"][0]["volumeInfo"]
    authors = book.get("authors", None)
    if authors:
        authors = ', '.join(authors)

    return {
        "author": authors,
        "title": book["title"],
        "ISBN": ISBN
    }


def is_valid_isbn(ISBN):
    """
    Return True if given value is a valid ISBN number, containing only numbers and has
    length of 10 or 13 characters.
    """

    if not isinstance(ISBN, str):
        return False

    if not re.search('^[0-9]+$', ISBN):
        return False

    return len(ISBN) == 10 or len(ISBN) == 13


def _get_book_details(ISBN):
    """ Get book details by ISBN from API """

    response = requests.get(f'{API_URL}?q=isbn:{ISBN}')

    if response.status_code != 200:
        raise RuntimeError("Api request to resolve book details failed")

    data = response.json()
    if data["totalItems"] == 0:
        return None
    return data
