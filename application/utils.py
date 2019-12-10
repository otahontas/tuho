import re

import requests


BOOK_API_URL = 'https://www.googleapis.com/books/v1/volumes'
VIDEO_API_URL = 'https://www.youtube.com/oembed'


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
        "image": book.get("imageLinks", {}).get("thumbnail", ""),
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

    response = requests.get(f'{BOOK_API_URL}?q=isbn:{ISBN}')

    if response.status_code != 200:
        raise RuntimeError("Api request to resolve book details failed")

    data = response.json()
    if data["totalItems"] == 0:
        return None
    return data


def get_video_title(link):
    """ Get video title for a given YouTube-link """
    response = requests.get(f'{VIDEO_API_URL}?format=json&url={link}')

    if response.status_code != 200:
        raise RuntimeError("Api request to resolve video details failed")

    data = response.json()
    return data.get('title', None)


def timestamp_parser(time):
    """ Convert minutes and seconds to seconds """

    if time:
        time = time.split(':')
        seconds = int(time[len(time) - 1])

        if len(time) > 1:
            for i in range(len(time) - 1):
                seconds += 60 * int(time[i])

        return seconds
    return time
