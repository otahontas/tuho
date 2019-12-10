def test_video_details(client, video):
    resp = client.get(f'/bookmark/{video.id}', follow_redirects=True)
    assert resp.status_code == 200

    data = str(resp.data)
    assert video.header in data
    assert video.comment.replace('\n', '\\n') in data


def test_video_details_with_timestamp(client, video):
    resp = client.get(f'/bookmark/{video.id}?timestamp=120', follow_redirects=True)
    assert resp.status_code == 200

    data = str(resp.data)
    assert '?start=120' in data
