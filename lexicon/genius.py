import requests
import json
import os
import sys
import re
from bs4 import BeautifulSoup

base_url = 'https://api.genius.com'
search_url = base_url + '/search'

def lyrics_from_song_api_path(song_api_path):
    """Return a list of cleaned lyrics.

    genius.com includes section headings, which I
    remove because they should not be included
    in the lyrics.
    """

    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json['response']['song']['path']
    page_url = 'https://genius.com' + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, 'html.parser')
    [h.extract() for h in html('script')]
    lyrics = html.find('div', {'class': 'lyrics'}).get_text()
    # this regex matches with all text enclosed by square brackets
    return re.sub(r'\n\[[^\]]*\]', '', lyrics)

def parse_album_file(album_file):
    """Return attributes from a JSON file detailing an album.

    read from a json file with attributes
    'artist': string
    'album': string
    'song': list of strings

    >>> artist, album, songs = parse_album_file('lyrics/vince/summertime06.json')
    >>> artist
    'Vince Staples'
    >>> album
    "Summertime '06"
    >>> len(songs)
    20
    """

    with open(album_file) as data_file:
        data = json.load(data_file)
    artist_name = data['artist']
    album_name = data['album']
    songs = data['songs']
    return artist_name, album_name, songs

if __name__ == '__main__':
    """
    command line arguments: album.json, target_directory
    $ python genius.py lyrics/kendrick/tpab.json lyrics/kendrick/tpab/
    that last slash / in target_directory is important
    """
    assert len(sys.argv) == 3, 'command line arguments: album.json, target_directory'
    _, album_file, target_directory = sys.argv
    TOKEN = os.environ['TOKEN']
    headers = {'Authorization': 'Bearer ' + TOKEN}
    artist_name, album_name, songs = parse_album_file(album_file)
    for i, song_title in enumerate(songs):
        print("Trying to retrieve {}".format(song_title))
        # query string sent as request
        data = {'q': song_title + ' ' + artist_name}
        response = requests.get(search_url, data=data, headers=headers)
        json = response.json()
        for hit in json['response']['hits']:
            if hit['result']['primary_artist']['name'] == artist_name:
                song_api_path = hit['result']['api_path']
                lyrics = lyrics_from_song_api_path(song_api_path)
                # file name 00.txt, 01.txt, and so on
                f = open(target_directory + "%02d" % (i,) + '.txt', 'w+')
                f.write(song_title + '\n')
                f.write(lyrics)
                f.close()
                print("Retrieved {}".format(song_title))
                break
