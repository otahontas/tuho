import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from application import app
from application.app import db
from application.models import Book
from pytest_bdd import scenario, given, when, then

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

"""Define cucumber tests here with BDD stylings"""

@scenario('add_book.feature', 'User added books are saved persistently')
def adding_works():
    pass

#@scenario('add_book.feature', 'User cannot add new books without specifying isbn, name and author')
#def test_adding_without_needed_details_does_not_work():
#    pass
#
#@scenario('add_book.feature', 'User cannot add a book twice with the same name')
#def test_adding_with_same_name_does_not_work():
#    pass
#
#@scenario('add_book.feature', 'User cannot add a book twice with the same isbn')
#def test_adding_with_same_isbn_does_not_work():
#    pass

@given("I have a new book with name, writer and isbn")
def create_book_with_needed_details():
    return Book(header='test', comment='comment', writer='test', ISBN=123)

#@given("I have a new book with only comment")
#def create_book_with_only_comment():
#    pass
#
#@given("I have a book with name that is already in db")
#def create_book_with_present_name():
#    pass
#
#@given("I have a book with isbn that is already in db")
#def create_book_with_present_isbn():
#    pass

@when("I try to add new book")
def add_new_book(create_book_with_needed_details):
    book = create_book_with_needed_details()
    db.session().add(book)
    db.session().commit()

@then("System will add book to db")
def check_book_is_in_db():
    fetched_book = Book.query.filter(Book.header == 'test').one()
    assert(fetched_book)

#@then("System will not add book to db")
#def check_book_not_in_db():
#    pass
