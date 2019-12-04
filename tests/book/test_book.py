def test_nonuniq_isbn_not_added(client):
    bookData = dict(header='Introduction to Algorithms',
                    writer='Thomas H. Cormen',
                    ISBN='9780262033848',
                    comment='comment')
    client.post('/bookmarks?prefilled=True', data=bookData, follow_redirects=True)
    rv = client.post('/bookmarks?prefilled=True', data=bookData, follow_redirects=True)
    assert b'Book with given ISBN was already in the database' in rv.data


def test_add_video_form(client):
    resp = client.get("/bookmarks/new")
    assert resp.status_code == 200

    data = str(resp.data)

    assert '<input type="submit" value="Add a new book"/>' in data
