import os
import tempfile
import time
from multiprocessing import Process

import pytest

from application import app, db
from application.factories import BookFactory, BookmarkFactory, VideoFactory

from selenium import webdriver


def bind_factories(session):
    # Hack(ish) solution to bind factories to db session
    BookmarkFactory._meta.sqlalchemy_session = session
    BookFactory._meta.sqlalchemy_session = session
    VideoFactory._meta.sqlalchemy_session = session


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    db_url = 'sqlite:///' + db_path
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config["SQLALCHEMY_ECHO"] = False
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            bind_factories(db.session)
        yield client

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def book():
    return BookFactory()


@pytest.fixture
def video():
    return VideoFactory()


@pytest.fixture
def browser():
    client = None
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    try:
        client = webdriver.Chrome(options=options)
    except Exception:
        pass

    if client:
        app_context = app.app_context()
        app_context.push()

        db_fd, db_path = tempfile.mkstemp()
        db_url = 'sqlite:///' + db_path
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
        app.config["SQLALCHEMY_ECHO"] = False
        app.config['TESTING'] = True

        server = Process(target=app.run)
        server.start()
        time.sleep(1)
        with app.app_context():
            db.drop_all()
            db.create_all()
            bind_factories(db.session)
        client.get('http://127.0.0.1:5000/')
        # time.sleep(2)
        yield client
        server.terminate()
        client.close()
        os.close(db_fd)
        os.unlink(db_path)
        app_context.pop()
