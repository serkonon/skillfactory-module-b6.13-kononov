import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist, album_name=""):
    """
    Находит альбомы по заданному артисту. Если album_name == "", возвращает все
    :param artist: имя артиста
    :param album_name: имя альбома
    :return: записи таблицы album
    """
    session = connect_db()
    if album_name:
        albums = session.query(Album). \
            filter(Album.artist == artist, Album.album == album_name).all()
    else:
        albums = session.query(Album).filter(Album.artist == artist).all()
    return albums


def save(album_data):
    """
    Сохраняет данные альбома
    :param album_data: Данные альбома
    :return: Текст ошибки в случае неуспешного сохранения, иначе - "OK"
    """
    album = Album(
        year=album_data["year"],
        artist=album_data["artist"],
        genre=album_data["genre"],
        album=album_data["album"]
    )
    result = check(album)
    if result == "OK":
        session = connect_db()
        session.add(album)
        session.commit()
    return result


def check(album):
    """
    Проверяет данные альбома
    :param row_data: Данные альбома
    :return: Текст ошибки в случае неуспешной проверки, иначе - "OK"
    """
    result = "Некорректное значение поля Год: {}".format(album.year)
    if album.year.isdigit():
        if int(album.year) in range(1800, 2020):
            result = "OK"
    return result

