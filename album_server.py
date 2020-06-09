from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album


@route("/albums/<artist>")
def albums(artist):
    """
    Выводит список альбомов данного артиста
    :param artist: Артист
    :return: Список альбомов атртиста. Если альбомы не найдены - ошибка 404
    """
    albums_list = album.find(artist)
    if albums_list:
        album_names = [alb.album for alb in albums_list]
        result = "<b>Список альбомов {} (всего {}):</b><br>".format(artist, len(album_names))
        result += "<br>".join(album_names)
    else:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)

    return result


@route('/albums')
def albums():
    return '''
        <form action="/albums" method="post">
            Год <input name="year" type="text" />
            Артист <input name="artist" type="text" />
            Жанр <input name="genre" type="text" />
            Альбом <input name="album" type="text" />
            <input value="Сохранить" type="submit" />
        </form>
    '''

@route("/albums", method="POST")
def albums_add():
    """
    Получает данные альбома методом POST и если нет такого
    альбома у такого артиста, добавляет его
    :return: Результат записи данных альбома
    """
    artist, album_name = request.forms.get("artist"), request.forms.get("album")
    album_data = {
        "year": request.forms.get("year"),
        "genre": request.forms.get("genre"),
        "artist": artist,
        "album": album_name
    }
    if album.find(artist, album_name):
        result = \
            HTTPError(409, "Данные не обновлены. Альбом {} артиста {} уже есть".
                      format(album_name, artist))
    else:
        result = album.save(album_data)
        if result == "OK":
            result = "Данные успешно сохранены"
        else:
            result = \
                HTTPError(422, "Данные не обновлены. " + result)

    return result


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)

