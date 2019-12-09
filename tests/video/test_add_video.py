from application.models import Video


def test_video_insertion(client):
    resp = client.post('/bookmarks/video', data={'header': 'test', 'URL': "",
                       'comment': 'comment'}, follow_redirects=True)
    assert resp.status_code == 200

    video = Video.query.one()
    assert video.header == "test"
    assert video.URL == ""
    assert video.comment == "comment"


def test_add_video_form(client):
    resp = client.get("/bookmarks/video")
    assert resp.status_code == 200

    data = str(resp.data)

    assert '<input type="submit" value="Add a new video"/>' in data
