from application.app import db


class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


class Bookmark(Base):
    __tablename__ = 'bookmark'

    TYPE_BOOK = 1
    TYPE_BLOG = 2
    TYPE_PODCAST = 3
    TYPE_VIDEO = 4

    read_status = db.Column(db.Boolean, default=False)
    read_date = db.Column(db.DateTime)
    header = db.Column(db.String(50))
    comment = db.Column(db.String(1024))
    type = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'bookmark'
    }


class Book(Bookmark):
    __tablename__ = 'book'

    def __init__(self, **kwargs):
        super(Book, self).__init__(**kwargs)
        self.type = Bookmark.TYPE_BOOK

    id = db.Column(db.Integer, db.ForeignKey('bookmark.id'), primary_key=True)
    ISBN = db.Column(db.String(17))
    writer = db.Column(db.String(250))

    __mapper_args__ = {
        'polymorphic_identity': 'book',
    }

    @staticmethod
    def delete(book_id):
        db.session.query(Book).filter(Book.id == book_id).delete()
        db.session.query(Bookmark).filter(Bookmark.id == book_id).delete()
        db.session.commit()


class Blog(Bookmark):
    __tablename__ = 'blog'

    def __init__(self, **kwargs):
        super(Blog, self).__init__(**kwargs)
        self.type = Bookmark.TYPE_BLOG

    id = db.Column(db.Integer, db.ForeignKey('bookmark.id'), primary_key=True)
    URL = db.Column(db.String(250))
    writer = db.Column(db.String(250))

    __mapper_args__ = {
        'polymorphic_identity': 'blog',
    }


class Podcast(Bookmark):
    __tablename__ = 'podcast'

    def __init__(self, **kwargs):
        super(Podcast, self).__init__(**kwargs)
        self.type = Bookmark.TYPE_PODCAST

    id = db.Column(db.Integer, db.ForeignKey('bookmark.id'), primary_key=True)
    name = db.Column(db.String(250))
    description = db.Column(db.String(1024))
    author = db.Column(db.String(250))

    __mapper_args__ = {
        'polymorphic_identity': 'podcast',
    }


class Video(Bookmark):
    __tablename__ = 'video'

    def __init__(self, **kwargs):
        super(Video, self).__init__(**kwargs)
        self.type = Bookmark.TYPE_VIDEO

    id = db.Column(db.Integer, db.ForeignKey('bookmark.id'), primary_key=True)
    URL = db.Column(db.String(250))

    __mapper_args__ = {
        'polymorphic_identity': 'video',
    }
