from flask_wtf import FlaskForm
from wtforms import StringField


class BookmarkForm(FlaskForm):
    header = StringField("Name")
    comment = StringField("Comment")

    class Meta:
        csrf = False


class BookForm(BookmarkForm):
    writer = StringField("Writer")
    ISBN = StringField("ISBN")