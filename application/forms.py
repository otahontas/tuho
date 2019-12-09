from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField
from wtforms.validators import URL, InputRequired, Length


class BookmarkForm(FlaskForm):
    header = StringField("Name", [Length(min=1, max=50)])
    comment = StringField("Comment", [Length(max=1024)])

    class Meta:
        csrf = False


class BookForm(BookmarkForm):
    writer = StringField("Writer", [Length(min=2, max=250)])
    ISBN = StringField("ISBN", [InputRequired()])
    image = StringField("Image URL")


class BookUpdateForm(BookForm):
    read_status = BooleanField("Read")


class VideoForm(BookmarkForm):
    URL = StringField("URL", [URL(require_tld=False)])
    timestamp = IntegerField("Timestamp")


class VideoUpdateForm(VideoForm):
    read_status = BooleanField("Read")
