# youtube-to-spotify
Download content from youtube and then import it as local media for spotify.

---
```
usage: main.py [-h] [-p PLAYLIST_ID] [-u PLAYLIST_URL] [-o OUTPUT_DIR]

Download music from any playlist on youtube

optional arguments:
  -h, --help            show this help message and exit
  -p PLAYLIST_ID, --playlist-id PLAYLIST_ID
                        id of playlist to download
  -u PLAYLIST_URL, --playlist-url PLAYLIST_URL
                        url of playlist to download
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        output directory to download songs in
```                        
---
Dependencies:
1. pip3 install google-api-python-client
2. pip3 install youtube_dl
