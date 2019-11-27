import os
import tempfile

import pytest

from application import app, db


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_empty_db(client):
    rv = client.get('/list')
    assert b'Tietokanta on tyhj' in rv.data


def test_book_insertion(client):
    rv = client.post('/bookmarks',
                     data=dict(
                         header='test',
                         writer='writer',
                         ISBN=123,
                         comment='comment'
                     ),
                     follow_redirects=True)
    assert b'test' in rv.data
    assert b'Tietokanta on tyhj' not in rv.data
