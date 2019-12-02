from flask import abort, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from application.app import app, db
from application.models import Book, Bookmark
from application.forms import BookForm

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
        assert Bookmark.query.get(bookmark_id)
    except (ValueError, AssertionError):
        abort(404)

    bookmark = db.session.query(Bookmark).get(bookmark_id)
    if not bookmark:
        abort(404)

    if bookmark.type == Bookmark.TYPE_BOOK:
        return render_template("bookmarks/book.html", book=bookmark)
    elif bookmark.type == Bookmark.TYPE_VIDEO:
        return render_template("bookmarks/video.html", book=bookmark)

    abort(404)


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
    form = BookForm()
    return render_template("bookmarks/new.html", form=form)


@app.route("/bookmarks", methods=["POST"])
def bookmarks_create():
    # TODO: If no ISBN given header and writer fields should be required
    form = BookForm(request.form)

    if is_valid_isbn(form.ISBN.data):
        try:
            book_details = resolve_book_details(form.ISBN.data)
            book = Book(header=book_details["title"], comment=form.comment.data,
                        writer=book_details["author"], ISBN=form.ISBN.data)
        except (RuntimeError, KeyError):
            # TODO Display error message, book fetch failed
            render_template("bookmarks/new.html", form=form, bookFetchFailed=True)
    else:
        book = Book(header=form.header.data, comment=form.comment.data,
                    writer=form.writer.data, ISBN=form.ISBN.data)

    db.session().add(book)
    try:
        db.session().commit()
    except IntegrityError:
        db.session.rollback()
        return render_template("/bookmarks/new.html", form=form, ISBN_taken=True)

    return redirect(url_for("bookmarks_list"))
