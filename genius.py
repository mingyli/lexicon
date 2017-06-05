import requests
import os
import sys
import re
from bs4 import BeautifulSoup

base_url = 'https://api.genius.com'
TOKEN = os.environ['TOKEN']
headers = {'Authorization': 'Bearer ' + TOKEN}

def lyrics_from_song_api_path(song_api_path):
    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json['response']['song']['path']
    page_url = 'https://genius.com' + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, 'html.parser')
    [h.extract() for h in html('script')]
    lyrics = html.find('div', {'class': 'lyrics'}).get_text()
    return re.sub(r'\n\[.*\]', '', lyrics)

def parse_album_file(album_file):
    txt = open(album_file)
    artist_name = txt.readline().strip()
    album_name = txt.readline().strip()
    songs = [line.strip() for line in txt]
    txt.close()
    return artist_name, album_name, songs

if __name__ == '__main__':
    """
    command line arguments: album.txt, target_directory
    """
    assert len(sys.argv) == 3
    _, album_file, target_directory = sys.argv
    artist_name, album_name, songs = parse_album_file(album_file)
    print(artist_name)
    print(album_name)
    print(songs)
    """
    search_url = base_url + '/search'
    data = {'q': song_title}
    response = requests.get(search_url, data=data, headers=headers)
    json = response.json()
    for hit in json['response']['hits']:
        if hit['result']['primary_artist']['name'] == artist_name:
            song_api_path = hit['result']['api_path']
            lyrics = lyrics_from_song_api_path(song_api_path)
            print(lyrics)
            break
            """
