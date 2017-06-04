import requests
import os
import re
from bs4 import BeautifulSoup

base_url = 'https://api.genius.com'
TOKEN = os.environ['TOKEN']
headers = {'Authorization': 'Bearer ' + TOKEN}
song_title = "Alright"
artist_name = "Kendrick Lamar"

def lyrics_from_song_api_path(song_api_path):
    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json['response']['song']['path']
    page_url = 'https://genius.com' + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, 'html.parser')
    [h.extract() for h in html('script')]
    # import pdb; pdb.set_trace()
    # lyrics = html.find('lyrics').get_text()
    lyrics = html.find('div', {'class': 'lyrics'}).get_text()
    return re.sub(r'\n\[.*\]', '', lyrics)

if __name__ == '__main__':
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
