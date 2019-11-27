import os
from application.app import db
from application.models import Book

if not os.environ.get("HEROKU"):
    db.drop_all()
    db.create_all()


def test_book_add():
    book = Book(header='test', comment='comment', writer='writer', ISBN=123)
    db.session().add(book)
    db.session().commit()
    fetched_book = Book.query.filter(Book.header == 'test').one()
    assert(fetched_book)


def test_book_removal():
    book = Book.query.filter(Book.header == 'test').one()
    Book.delete(book.id)
    fetched_books = Book.query.filter(Book.header == 'test').all()
    assert(len(fetched_books) == 0)
