import re

from flask import abort, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError
from sqlalchemy_filters import apply_filters, apply_pagination

from application.app import app, db
from application.forms import UpdateCommentForm, UpdateTimestampForm
from application.models import Bookmark


@app.route("/")
def index():
    return redirect(url_for("bookmarks_list"))


@app.route("/list", methods=["GET"])
def bookmarks_list():
    page = request.args.get('page', 1, type=int)
    filter_type = request.args.get('type', type=int)
    filter_seen = request.args.get('seen', type=int)

    bookmarks = Bookmark.query
    types = list({(b.__class__.__name__, b.type) for b in bookmarks})

    filter_spec = []

    if filter_type:
        filter_spec.append({'field': 'type', 'op': '==', 'value': filter_type})
    if filter_seen:
        if filter_seen == 1:
            op = '=='
        elif filter_seen == 2:
            op = '!='
        filter_spec.append({'field': 'read_status', 'op': op, 'value': True})

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
        comment_form = UpdateCommentForm()
        comment_form.comment.data = bookmark.comment
        return render_template("bookmarks/book/details.html", book=bookmark,
                               comment_form=comment_form)
    elif bookmark.type == Bookmark.TYPE_VIDEO:
        comment_form = UpdateCommentForm()
        comment_form.comment.data = bookmark.comment
        timestamp_form = UpdateTimestampForm()
        timestamp_form.timestamp.data = bookmark.timestamp

        yt = "https://www.youtube-nocookie.com/embed/"
        timestamp = request.args.get('timestamp')
        # substitute non-ID part with embed-URL
        embed = re.sub(r'http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)' +
                       r'(&(amp;)?[\w\?=]*)?', yt, bookmark.URL)
        timestamp = request.args.get('timestamp')
        if timestamp:
            embed += '?start=' + str(timestamp)

        return render_template("bookmarks/video/details.html", video=bookmark,
                               embed=embed, comment_form=comment_form,
                               timestamp_form=timestamp_form)

    abort(404)


@app.route("/bookmark/delete/<bookmark_id>", methods=["GET"])
def delete_bookmark(bookmark_id):
    Bookmark.query.get_or_404(bookmark_id)  # To check if bookmark is found on db

    db.session.query(Bookmark).filter(Bookmark.id == bookmark_id).delete()
    db.session.commit()

    return redirect(url_for("bookmarks_list"))


@app.route("/bookmarks/edit/<bookmark_id>", methods=["GET"])
def bookmarks_edit(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)

    if bookmark.type == Bookmark.TYPE_BOOK:
        return redirect(url_for("book_update", book_id=bookmark_id, bookmark=bookmark))
    elif bookmark.type == Bookmark.TYPE_VIDEO:
        return redirect(url_for("video_update", video_id=bookmark_id, bookmark=bookmark))

    abort(404)


@app.route("/bookmarks/edit/comment/<bookmark_id>", methods=["POST"])
def update_comment(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    form = UpdateCommentForm()

    if form.validate_on_submit():
        bookmark.comment = form.comment.data
        try:
            db.session().commit()
        except IntegrityError:
            db.session.rollback()

    return redirect(url_for("get_bookmark", bookmark_id=bookmark_id))
