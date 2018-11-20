from app import app
import sqlite3 as sq3
from sqlite3 import Error
from flask import jsonify, request


def create_connection(database):
    try:
        conn = sq3.connect(database)
        cur = conn.cursor()
        return cur
    except Error as e:
        print(e)


@app.route('/')
@app.route('/index')
def index():
    # TODO html for index page.
    return 'Welcome to The Music Info Place'


@app.route('/music/artists/all', methods=['GET'])
def artists_all():
    sql = 'SELECT name FROM artists'
    cur = create_connection('data.db')
    result = cur.execute(sql).fetchall()
    return jsonify(result)


@app.route('/music/artists', methods=['GET'])
def artist_albums():
    query_parameters = request.args
    query = query_parameters.get('name')
    sql = """
    SELECT title
    FROM albums
    INNER JOIN  artists ON artists.ArtistId = albums.ArtistId
    WHERE  artists.Name = ?;"""

    cur = create_connection('data.db')
    result = cur.execute(sql, ('{}'.format(query),)).fetchall()
    if len(result):
        return jsonify(result)
    else:
        return 'Sorry! We don\'t have info on that artist.'


@app.route('/music/albums/all', methods=['GET'])
def albums_all():
    sql = """
    SELECT Title FROM albums"""
    cur = create_connection('data.db')
    result = cur.execute(sql).fetchall()
    return jsonify(result)


@app.route('/music/albums', methods=['GET'])
def album_tracks():
    query_params = request.args
    query = query_params.get('title')
    sql = """
    SELECT tracks.GenreId, name
    FROM tracks
    INNER JOIN albums ON albums.AlbumId = tracks.AlbumId
    WHERE albums.Title = ?;"""

    cur = create_connection('data.db')
    result = cur.execute(sql, ('{}'.format(query),)).fetchall()
    if len(result):
        return jsonify(result)
    else:
        return 'Sorry! We don\'t have info on that album.'


@app.route('/music/tracks/all', methods=['GET'])
def tracks_all():
    sql = """
    SELECT name FROM tracks"""
    cur = create_connection('data.db')
    result = cur.execute(sql).fetchall()
    return jsonify(result)
