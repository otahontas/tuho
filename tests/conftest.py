import os
import tempfile

import pytest

from application import app, db


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    db_url = 'sqlite:///' + db_path
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(db_path)
