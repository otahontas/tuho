import factory

from .models import Book, Bookmark, Video


class BookmarkFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: '%s' % n)
    header = factory.Faker('sentence', nb_words=4, variable_nb_words=True,
                           ext_word_list=None)
    comment = factory.Faker('text', max_nb_chars=200, ext_word_list=None)

    class Meta:
        model = Bookmark
        sqlalchemy_session_persistence = 'commit'


class BookFactory(BookmarkFactory):
    ISBN = factory.Faker('isbn13', separator="")
    writer = factory.Faker('name')

    class Meta:
        model = Book
        sqlalchemy_session_persistence = 'commit'


class VideoFactory(BookFactory):
    URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    class Meta:
        model = Video
        sqlalchemy_session_persistence = 'commit'
