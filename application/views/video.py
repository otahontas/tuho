from flask import redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from application.app import app, db
from application.forms import VideoForm
from application.models import Bookmark, Video


@app.route("/bookmarks/new/video")
def video_form():
    form = VideoForm()
    return render_template("bookmarks/video/new.html", form=form)


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
        return render_template("/bookmarks/video/new.html")

    return redirect(url_for("bookmarks_list"))


@app.route("/bookmarks/video/edit/<video_id>", methods=["GET", "POST"])
def video_update(video_id, bookmark=None):
    if not bookmark:
        video = Bookmark.query.get_or_404(video_id)

    if request.method == "GET":
        form = VideoForm()
        form.header.data = video.header
        form.comment.data = video.comment
        form.URL.data = video.URL
        form.timestamp.data = video.timestamp
        return render_template("bookmarks/video/edit.html", form=form,
                               video_id=video_id)

    form = VideoForm(request.form)
    # TODO: validate form

    video.header = form.header.data
    video.URL = form.URL.data
    video.timestamp = form.timestamp.data
    video.comment = form.comment.data

    try:
        db.session().commit()
    except IntegrityError:
        db.session.rollback()
        return render_template("update/video/edit.html", form=form,
                               video_id=video_id)

    return redirect(url_for("get_bookmark", bookmark_id=video_id))
