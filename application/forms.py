from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, TextAreaField
from wtforms.validators import URL, InputRequired, Length, Optional


class BookmarkForm(FlaskForm):
    header = StringField("Name", [Length(min=1, max=50)])
    comment = TextAreaField("Comment", [Length(max=1024)])

    class Meta:
        csrf = False


class BookForm(BookmarkForm):
    writer = StringField("Writer", [Length(min=2, max=250)])
    ISBN = StringField("ISBN", [InputRequired()])
    image = StringField("Image URL")


class BookUpdateForm(BookForm):
    read_status = BooleanField("Read")


class VideoForm(BookmarkForm):
    URL = StringField("URL", [InputRequired(), URL(require_tld=False)])
    timestamp = StringField("Timestamp", [Optional()])


class VideoUpdateForm(VideoForm):
    read_status = BooleanField("Read")


class UpdateCommentForm(FlaskForm):
    comment = TextAreaField("Comment", [Length(max=1024)])

    class Meta:
        csrf = False


class UpdateTimestampForm(FlaskForm):
    timestamp = StringField("Timestamp")

    class Meta:
        csrf = False
