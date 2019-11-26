from flask import redirect, render_template, request, url_for

from application.app import app, db
from application.models import Book, Bookmark


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
    except ValueError:
        return redirect(url_for("bookmarks_list"))

    # TODO: Handle if no bookmark found sqlalchemy.orm.exc.NoResultFound
    bookmark = Bookmark.query.get(bookmark_id)

    if bookmark is None:
        return redirect(url_for("bookmarks_list"))

    if bookmark.type == 1:
        Book.query.filter(Book.id == bookmark_id).delete()
    else:
        return redirect(url_for("bookmarks_list"))

    db.session.delete(bookmark)
    db.session.commit()
    return redirect(url_for("bookmarks_list"))


@app.route("/bookmarks/new")
def bookmarks_form():
    return render_template("bookmarks/new.html")


@app.route("/bookmarks", methods=["POST"])
def bookmarks_create():
    header = request.form.get("header")
    comment = request.form.get("comment")
    writer = request.form.get("writer")
    ISBN = request.form.get("ISBN")

    book = Book(header=header, comment=comment, writer=writer, ISBN=ISBN)

    db.session().add(book)
    db.session().commit()

    return redirect(url_for("bookmarks_list"))
