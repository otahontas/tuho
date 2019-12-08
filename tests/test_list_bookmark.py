def test_empty_db(client):
    response = client.get('/list')
    assert response.status_code == 200
    assert b'No bookmarks' in response.data


def test_with_one_book(client, book):
    response = client.get('/list')
    assert response.status_code == 200

    # Workaround as bytes object does not accept .format()
    test_pattern = f"{book.header}"
    assert test_pattern.encode() in response.data


def test_no_books_shown_when_filtering_with_videos(client, book):
    response = client.get('/list?type=4')
    assert response.status_code == 200
    assert b'No bookmarks' in response.data
