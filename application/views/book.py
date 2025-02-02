import re

from flask import flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from application.app import app, db
from application.forms import BookForm, BookUpdateForm
from application.models import Book, Bookmark

from ..utils import is_valid_isbn, resolve_book_details


@app.route("/bookmarks/book", methods=["GET", "POST"])
def book_create():
    form = BookForm()

    if request.method == "GET":
        return render_template("bookmarks/book/new.html", form=form)

    prefilled = request.args.get('prefilled')
    form.ISBN.data = re.sub(r'[^\d]*', '', form.ISBN.data)

    if is_valid_isbn(form.ISBN.data):
        if not prefilled:
            try:
                book_details = resolve_book_details(form.ISBN.data)
                form.header.data = book_details.get("title")
                form.writer.data = book_details.get("author")
                form.image.data = book_details.get("image")
                flash('Name and writer resolved successfully, ' +
                      'please check that details are correct')
                return render_template("/bookmarks/book/new.html", form=form,
                                       prefilled=True)
            except (RuntimeError):
                flash('Book fetch failed, please give name and title for book yourself')
                return render_template("/bookmarks/book/new.html", form=form,
                                       prefilled=True)
        else:
            book = Book(header=form.header.data, writer=form.writer.data,
                        comment=form.comment.data, ISBN=form.ISBN.data,
                        image=form.image.data)
    else:
        flash('ISBN given was not valid, please give a valid ISBN instead')
        return render_template("/bookmarks/book/new.html", form=form)

    if form.validate_on_submit():
        db.session().add(book)
        try:
            db.session().commit()
        except IntegrityError:
            db.session.rollback()
            flash('Book with given ISBN was already in the database')
            return render_template("/bookmarks/book/new.html", form=form)

        flash('Book succefully added')
        return redirect(url_for("get_bookmark", bookmark_id=book.id))
    else:
        return render_template("bookmarks/book/new.html", form=form)


@app.route("/bookmarks/book/edit/<book_id>", methods=["GET", "POST"])
def book_update(book_id, bookmark=None):
    if not bookmark:
        bookmark = Bookmark.query.get_or_404(book_id)

    form = BookUpdateForm()

    if form.validate_on_submit():
        bookmark.header = form.header.data
        bookmark.writer = form.writer.data
        bookmark.comment = form.comment.data
        bookmark.image = form.image.data
        bookmark.ISBN = form.ISBN.data
        bookmark.read_status = form.read_status.data

        try:
            db.session().commit()
        except IntegrityError:
            db.session.rollback()
            return render_template("bookmarks/book/edit.html", form=form,
                                   bookmark_id=book_id, ISBN_taken=True)

        return redirect(url_for("get_bookmark", bookmark_id=book_id))

    form.header.data = bookmark.header
    form.comment.data = bookmark.comment
    form.writer.data = bookmark.writer
    form.ISBN.data = bookmark.ISBN
    form.image.data = bookmark.image
    form.read_status.data = bookmark.read_status
    return render_template("bookmarks/book/edit.html", form=form,
                           bookmark_id=book_id)
