from application.app import db


def test_book_details_view(client, book):
    resp = client.get(f"/bookmark/{book.id}")
    assert resp.status_code == 200

    data = str(resp.data)

    assert book.header in data
    assert book.writer in data
    assert book.comment.replace('\n', '\\n') in data
    assert book.image in data
    assert 'cover-placeholder.jpg' not in data


def test_book_details_without_image(client, book):
    book.image = None
    db.session.add(book)
    db.session.commit()

    resp = client.get(f"/bookmark/{book.id}")
    assert resp.status_code == 200

    data = str(resp.data)
    assert 'cover-placeholder.jpg' in data


def test_video_details(client, video):
    resp = client.get(f"/bookmark/{video.id}")
    assert resp.status_code == 200

    data = str(resp.data)

    assert video.header in data
    assert video.comment.replace('\n', '\\n') in data


def test_invalid_book_details_view(client, book):
    resp = client.get(f"/bookmark/-1")
    assert resp.status_code == 404
