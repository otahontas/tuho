import pytest


@pytest.fixture
def mock_failed_status_code(mocker):
    mock = mocker.Mock()
    mocker.patch('application.utils.requests', mock)
    mock.get.return_value.status_code = 404
    return mock


@pytest.fixture
def mock_succesful_api_fetch(mocker):
    mock = mocker.Mock()
    mocker.patch('application.utils.requests', mock)
    mock.get.return_value.status_code = 200
    mock.get.return_value.json.return_value = {
        "totalItems": 1,
        "items": [
            {
                "volumeInfo": {
                    "title": "Introduction to Algorithms",
                    "authors": ["Thomas H. Cormen"],
                    "ISBN": "9780262033848"
                }
            }
        ]
    }
    return mock


def test_nonuniq_isbn_not_added(client):
    bookData = dict(header='Introduction to Algorithms',
                    writer='Thomas H. Cormen',
                    ISBN='9780262033848',
                    comment='comment')
    client.post('/bookmarks?prefilled=True', data=bookData, follow_redirects=True)
    rv = client.post('/bookmarks?prefilled=True', data=bookData, follow_redirects=True)
    assert b'Book with given ISBN was already in the database' in rv.data


def test_nonvalid_isbn_is_not_added_and_error_is_shown(client):
    bookData = dict(ISBN='9780033')
    rv = client.post('/bookmarks', data=bookData, follow_redirects=True)
    assert b'ISBN given was not valid, please give a valid ISBN instead' in rv.data


@pytest.mark.usefixtures("mock_failed_status_code")
def test_valid_but_nonexisting_isbn_is_not_added_and_error_is_shown(client):
    bookData = dict(ISBN='9999999999')
    rv = client.post('/bookmarks', data=bookData, follow_redirects=True)
    assert b'Book fetch failed, please give name and title for book yourself' in rv.data


def test_isbn_changed_to_nonvalid_after_prefilling_is_not_added(client):
    bookData = dict(header='Introduction to Algorithms',
                    writer='Thomas H. Cormen',
                    ISBN='9780',
                    comment='comment')
    rv = client.post('/bookmarks?prefilled=True', data=bookData, follow_redirects=True)
    assert b'ISBN given was not valid, please give a valid ISBN instead' in rv.data


def test_bookform_is_rendered_correctly(client):
    rv = client.get('/bookmarks/new')
    assert b'Name' in rv.data
    assert b'Writer' in rv.data
    assert b'ISBN' in rv.data
    assert b'Comment' in rv.data
    assert b'<input type="submit" value="Add a new book"/>' in rv.data



@pytest.mark.usefixtures("mock_succesful_api_fetch")
def test_correct_details_are_prefilled_correctly(client):
    bookData = dict(ISBN='9780262033848')
    rv = client.post('/bookmarks', data=bookData, follow_redirects=True)
    assert b'Introduction to Algorithms' in rv.data
    assert b'Thomas H. Cormen' in rv.data
