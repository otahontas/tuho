from urllib.error import HTTPError

from flask import flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from application.app import app, db
from application.forms import VideoForm, VideoUpdateForm
from application.models import Bookmark, Video

from ..utils import get_video_title, timestamp_parser


@app.route("/bookmarks/video", methods=["GET", "POST"])
def video_create():
    form = VideoForm()

    if request.method == "GET":
        return render_template("bookmarks/video/new.html", form=form)

    if not form.header.data:
        try:
            title = get_video_title(form.URL.data)
            form.header.data = title
            flash('Title updated')
            return render_template("bookmarks/video/new.html", form=form)
        except (RuntimeError, HTTPError):
            flash('Check the link')
            return render_template("bookmarks/video/new.html", form=form)

    if form.validate_on_submit():
        video = Video(header=form.header.data,
                      comment=form.comment.data,
                      URL=form.URL.data,
                      timestamp=timestamp_parser(form.timestamp.data))

        db.session().add(video)
        try:
            db.session().commit()
        except IntegrityError:
            db.session.rollback()
            return render_template("/bookmarks/video/new.html")
        return redirect(url_for("get_bookmark", bookmark_id=video.id))

    return render_template("bookmarks/video/new.html", form=form)


@app.route("/bookmarks/video/edit/<video_id>", methods=["GET", "POST"])
def video_update(video_id, bookmark=None):
    if not bookmark:
        video = Bookmark.query.get_or_404(video_id)

    form = VideoUpdateForm()

    if form.validate_on_submit():
        video.header = form.header.data
        video.URL = form.URL.data
        video.timestamp = form.timestamp.data
        video.comment = form.comment.data
        video.read_status = form.read_status.data

        try:
            db.session().commit()
        except IntegrityError:
            db.session.rollback()
            return render_template("update/video/edit.html", form=form,
                                   video_id=video_id)

        return redirect(url_for("get_bookmark", bookmark_id=video_id))

    form.header.data = video.header
    form.comment.data = video.comment
    form.URL.data = video.URL
    form.timestamp.data = video.timestamp
    form.read_status.data = video.read_status
    return render_template("bookmarks/video/edit.html", form=form,
                           video_id=video_id)
