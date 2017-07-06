## [`genius.py`](genius.py)

uses BeautifulSoup and Genius API to retrieve lyrics 

requires a Genius API token. I set mine as an environment variable using `export TOKEN=<token>`

### Usage

`genius.py` requires a JSON file that details an album, such as [`bigfishtheory.json`](lyrics/vince/bigfishtheory.json)

```javascript
{
    "artist": "Vince Staples",
    "album": "Big Fish Theory",
    "songs": [
        "Crabs in a Bucket (Ft. Kilo Kish)",
        "Big Fish (Ft. Juicy J)",
        "Alyssa Interlude",
        "Love Can Be...",
        "745",
        "Ramona Park Is Yankee Stadium",
        "Yeah Right",
        "Homage",
        "SAMO",
        "Party People",
        "BagBak",
        "Rain Come Down"
    ]
}
```

then run `genius.py` with the JSON file and a directory as arguments

`python genius.py bigfishtheory.json lyrics/vince/bigfishtheory/`

## [`music.py`](music.py)

easily create artist corpora.

### Usage

As with `genius.py`, `music.py` requires the same JSON file that details an album. The lyrics should be first retrieved using `genius.py`.

```python
damn = Album('lyrics/kendrick/damn.json')
```

An `Album` is composed of its `Song`s. `Album`s can be iterated over. Both classes support various text collection operations.

```python
word = "phone"
for song in damn:
    print(song.title, " has ", song.count(word), " counts of ", word)

wordcount = sum(len(song) for song in damn)
assert wordcount == len(damn.words)
```
