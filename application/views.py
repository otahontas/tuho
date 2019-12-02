from flask import abort, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from application.app import app, db
from application.models import Book, Bookmark

from .utils import is_valid_isbn, resolve_book_details


@app.route("/")
def index():
    return redirect(url_for("bookmarks_list"))


@app.route("/list", methods=["GET"])
def bookmarks_list():
    page = request.args.get('page', 1, type=int)
    bookmarks = Bookmark.query.order_by(Bookmark.header).paginate(page, 5, False)
    next_url = url_for('bookmarks_list', page=bookmarks.next_num) \
        if bookmarks.has_next else None
    prev_url = url_for('bookmarks_list', page=bookmarks.prev_num) \
        if bookmarks.has_prev else None
    return render_template("list.html", bookmarks=bookmarks, next_url=next_url,
                           prev_url=prev_url, current=page)


@app.route("/bookmark/<bookmark_id>", methods=["GET"])
def get_bookmark(bookmark_id):
    try:
        int(bookmark_id)
    except ValueError:
        return render_template("bookmark.html")

    # TODO: Handle if no bookmark found sqlalchemy.orm.exc.NoResultFound
    bookmark = Bookmark.query.get(bookmark_id)

    if bookmark is None:
        return render_template("bookmark.html")

    # TODO: Create bookmark.html template
    return render_template("bookmark.html", bookmark=bookmark)


@app.route("/bookmark/delete/<bookmark_id>", methods=["GET"])
def delete_bookmark(bookmark_id):
    try:
        int(bookmark_id)
        assert Bookmark.query.get(bookmark_id)
    except (ValueError, AssertionError):
        abort(404)

    db.session.query(Bookmark).filter(Bookmark.id == bookmark_id).delete()
    db.session.commit()

    return redirect(url_for("bookmarks_list"))


@app.route("/bookmarks/new")
def bookmarks_form():
    return render_template("bookmarks/new.html")


@app.route("/bookmarks", methods=["POST"])
def bookmarks_create():
    # TODO: Should this be refactored to use wtforms?
    # TODO: If no ISBN given header and writer fields should be required
    ISBN = request.form.get("ISBN", None)
    comment = request.form.get("comment", None)
    if is_valid_isbn(ISBN):
        try:
            book_details = resolve_book_details(ISBN)
            book = Book(header=book_details["title"], comment=comment,
                        writer=book_details["author"], ISBN=ISBN)
        except (RuntimeError, KeyError):
            # TODO Display error message, book fetch failed
            render_template("bookmarks/new.html", bookFetchFailed=True)
    else:
        header = request.form.get("header", None)
        writer = request.form.get("writer", None)
        book = Book(header=header, comment=comment, writer=writer, ISBN=ISBN)

    db.session().add(book)
    try:
        db.session().commit()
    except IntegrityError:
        db.session.rollback()
        return render_template("/bookmarks/new.html", ISBN_taken=True)

    return redirect(url_for("bookmarks_list"))
