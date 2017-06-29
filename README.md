## [`genius.py`](genius.py)

uses BeautifulSoup and Genius API to retrieve lyrics 

requires a Genius API token. I set mine as an environment variable using `export TOKEN=<token>`

### Usage

`genius.py` requires a JSON file that details an album, such as [`bigfishtheory.json`](lyrics/vince/bigfishtheory.json)

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

then run

`$ python genius.py lyrics/vince/bigfishtheory.json lyrics/vince/bigfishtheory/`
