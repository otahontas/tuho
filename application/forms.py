from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField


class BookmarkForm(FlaskForm):
    header = StringField("Name")
    comment = StringField("Comment")

    class Meta:
        csrf = False


class BookForm(BookmarkForm):
    writer = StringField("Writer")
    ISBN = StringField("ISBN")


class BookUpdateForm(BookForm):
    read_status = BooleanField("Read")


class VideoForm(BookmarkForm):
    URL = StringField("URL")
    timestamp = IntegerField("Timestamp")
