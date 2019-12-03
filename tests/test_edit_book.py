def test_edit_book(client, book):
    """ Assert that book instance is edited """
    response = client.post(f"/bookmarks/edit/{book.id}",
                           data=dict(
                               header="test_header",
                               writer="writer",
                               ISBN=123,
                               comment="comment"
                           ),
                           follow_redirects=True)
    assert response.status_code == 200
    assert b"test_header" in response.data


def test_edit_non_exists_book(client):
    """ Assert that both book and bookmark instance is deleted """
    response = client.get(f"/bookmark/edit/-1")
    assert response.status_code == 404
