
from application.models import Video


def test_edit_form(client, video):
    resp = client.get(f"/bookmarks/edit/{video.id}")
    assert resp.status_code == 200

    data = str(resp.data)

    assert '<input type="submit" value="Update video"/>' in data


def test_edit_video(client, video):
    resp = client.post(f"/bookmarks/video/edit/{video.id}",
                       data={'header': 'Updated name'}, follow_redirects=True)
    assert resp.status_code == 200

    video = Video.query.one()
    assert video.header == 'Updated name'


def test_edit_video_invalid_id(client, video):
    resp = client.post("/bookmarks/video/edit/-1", data={'header': 'Updated name'},
                       follow_redirects=True)
    assert resp.status_code == 404

    video = Video.query.one()
    assert not video.header == 'Updated name'
