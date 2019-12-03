import re

from flask import abort, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError
from sqlalchemy_filters import apply_filters, apply_pagination

from application.app import app, db
from application.forms import BookForm, BookUpdateForm, VideoForm
from application.models import Book, Bookmark, Video

from .utils import is_valid_isbn, resolve_book_details


@app.route("/")
def index():
    return redirect(url_for("bookmarks_list"))


@app.route("/list", methods=["GET"])
def bookmarks_list():
    page = request.args.get('page', 1, type=int)
    filter_type = request.args.get('type', type=int)

    bookmarks = Bookmark.query
    types = list({(b.__class__.__name__, b.type) for b in bookmarks})

    if filter_type:
        filter_spec = [{'field': 'type', 'op': '==', 'value': filter_type}]
        bookmarks = apply_filters(bookmarks, filter_spec)

    bookmarks, pagination = apply_pagination(bookmarks, page_number=page,
                                             page_size=5)

    page = pagination.page_number
    next_url = url_for('bookmarks_list', page=page + 1) \
        if page < pagination.num_pages else None
    prev_url = url_for('bookmarks_list', page=page - 1) \
        if page > 1 else None

    return render_template("list.html", bookmarks=bookmarks, types=types,
                           next_url=next_url, prev_url=prev_url, current=page)


@app.route("/bookmark/<bookmark_id>", methods=["GET"])
def get_bookmark(bookmark_id):
    try:
        int(bookmark_id)
        assert Bookmark.query.get(bookmark_id)
    except (ValueError, AssertionError):
        abort(404)
    bookmark = db.session.query(Bookmark).get(bookmark_id)

    if bookmark.type == Bookmark.TYPE_BOOK:
        return render_template("bookmarks/book.html", book=bookmark)
    elif bookmark.type == Bookmark.TYPE_VIDEO:
        yt = "https://www.youtube-nocookie.com/embed/"
        timestamp = request.args.get('timestamp')
        # substitute non-ID part with embed-URL
        embed = re.sub(r'http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)' +
                       r'(&(amp;)?[\w\?=]*)?', yt, bookmark.URL)
        timestamp = request.args.get('timestamp')
        print("timestamp: ", timestamp)
        if timestamp:
            embed += '?start=' + str(timestamp)
        print(embed)
        return render_template("bookmarks/video.html", video=bookmark, embed=embed)

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
            book = Book(header=book_details["title"],
                        comment=form.comment.data,
                        writer=book_details["author"], ISBN=form.ISBN.data)
        except (RuntimeError, KeyError):
            # TODO Display error message, book fetch failed
            render_template("bookmarks/new.html", form=form,
                            bookFetchFailed=True)
    else:
        book = Book(header=form.header.data, comment=form.comment.data,
                    writer=form.writer.data, ISBN=form.ISBN.data)

    db.session().add(book)
    try:
        db.session().commit()
    except IntegrityError:
        db.session.rollback()
        return render_template("/bookmarks/new.html", form=form,
                               ISBN_taken=True)

    return redirect(url_for("bookmarks_list"))


@app.route("/bookmarks/edit/<bookmark_id>", methods=["GET"])
def bookmarks_edit(bookmark_id):
    try:
        int(bookmark_id)
        assert Bookmark.query.get(bookmark_id)
    except (ValueError, AssertionError):
        abort(404)

    bookmark = db.session.query(Bookmark).get(bookmark_id)

    if bookmark.type == Bookmark.TYPE_BOOK:
        form = BookUpdateForm()
        form.header.data = bookmark.header
        form.comment.data = bookmark.comment
        form.writer.data = bookmark.writer
        form.ISBN.data = bookmark.ISBN
        form.read_status.data = bookmark.read_status
        return render_template("bookmarks/update.html", form=form,
                               bookmark_id=bookmark_id)

    if bookmark.type == Bookmark.TYPE_VIDEO:
        form = VideoForm()
        form.header.data = bookmark.header
        form.comment.data = bookmark.comment
        form.URL.data = bookmark.URL
        form.timestamp.data = bookmark.timestamp
        return render_template("bookmarks/update/video.html", form=form,
                               video_id=bookmark_id)

    abort(404)


@app.route("/bookmarks/edit/<bookmark_id>", methods=["POST"])
def bookmarks_update(bookmark_id):
    try:
        int(bookmark_id)
        assert Bookmark.query.get(bookmark_id)
    except (ValueError, AssertionError):
        abort(404)

    bookmark = db.session.query(Bookmark).get(bookmark_id)

    form = BookUpdateForm(request.form)

    if is_valid_isbn(form.ISBN.data):
        try:
            book_details = resolve_book_details(form.ISBN.data)
            bookmark.header = book_details["title"]
            bookmark.writer = book_details["author"]
            bookmark.comment = form.writer.data
            bookmark.ISBN = form.ISBN.data
            bookmark.read_status = form.read_status.data
        except (RuntimeError, KeyError):
            # TODO Display error message, book fetch failed
            return render_template("bookmarks/update.html", form=form,
                                   bookmark_id=bookmark_id,
                                   bookFetchFailed=True)
    else:
        bookmark.header = form.header.data
        bookmark.writer = form.writer.data
        bookmark.comment = form.comment.data
        bookmark.ISBN = form.ISBN.data
        bookmark.read_status = form.read_status.data

    try:
        db.session().commit()
    except IntegrityError:
        db.session.rollback()
        return render_template("bookmarks/update.html", form=form,
                               bookmark_id=bookmark_id, ISBN_taken=True)

    return redirect(url_for("get_bookmark", bookmark_id=bookmark_id))


@app.route("/bookmarks/new/video")
def video_form():
    form = VideoForm()
    return render_template("bookmarks/new/video.html", form=form)


@app.route("/bookmarks/video", methods=["POST"])
def video_create():
    form = VideoForm(request.form)

    video = Video(header=form.header.data,
                  comment=form.comment.data,
                  URL=form.URL.data,
                  timestamp=form.timestamp.data)

    db.session().add(video)
    try:
        db.session().commit()
    except IntegrityError:
        db.session.rollback()
        return render_template("/bookmarks/new/video.html")

    return redirect(url_for("bookmarks_list"))


@app.route("/bookmarks/video/edit/<video_id>", methods=["POST"])
def video_update(video_id):
    try:
        int(video_id)
        assert Bookmark.query.get(video_id)
    except (ValueError, AssertionError):
        abort(404)

    video = db.session.query(Bookmark).get(video_id)

    form = VideoForm(request.form)

    video.header = form.header.data
    video.URL = form.URL.data
    video.timestamp = form.timestamp.data
    video.comment = form.comment.data

    try:
        db.session().commit()
    except IntegrityError:
        db.session.rollback()
        return render_template("update/video.html", form=form,
                               video_id=video_id)

    return redirect(url_for("get_bookmark", bookmark_id=video_id))
