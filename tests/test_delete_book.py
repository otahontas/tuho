from application.models import Book, Bookmark


def test_delete_book(client, book):
    """ Assert that both book and bookmark instabce is deleted """
    response = client.get(f"/bookmark/delete/{book.id}", follow_redirects=True)
    assert response.status_code == 200
    assert Book.query.count() == 0
    assert Bookmark.query.count() == 0


def test_delete_non_exists_book(client):
    """ Assert that both book and bookmark instabce is deleted """
    response = client.get(f"/bookmark/delete/-1")
    assert response.status_code == 404
