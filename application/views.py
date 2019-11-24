from flask import render_template, request, url_for

from application.app import app
from application.models import Book, Bookmark


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/list", methods=["GET"])
def bookmarks_list():
    page = request.args.get('page', 1, type=int)
    bookmarks = Book.query.order_by(Book.header).paginate(page, 5, False)
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
