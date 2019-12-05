def test_edit_book(client, book):
    """ Assert that book instance is edited """
    response = client.post(f"/bookmarks/book/edit/{book.id}",
                           data=dict(
                               header="test_header",
                               writer="writer",
                               ISBN=123,
                               comment="comment"
                           ),
                           follow_redirects=True)
    assert response.status_code == 200
    assert b"test_header" in response.data


def test_edit_form_non_exists_book(client):
    response = client.get(f"/bookmarks/book/edit/-1", follow_redirects=True)
    assert response.status_code == 404


def test_edit_non_exists_book(client):
    response = client.post(f"/bookmarks/book/edit/-1", data={}, follow_redirects=True)
    assert response.status_code == 404


def test_edit_form(client, book):
    resp = client.get(f"/bookmarks/book/edit/{book.id}", follow_redirects=True)
    assert resp.status_code == 200

    data = str(resp.data)

    assert '<input type="submit" value="Update book"/>' in data
