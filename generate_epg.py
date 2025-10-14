import requests
from bs4 import BeautifulSoup
import datetime
import html

# Correct URL
url = "https://radio-online.my/988-fm-playlist"

# Get page HTML
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
r = requests.get(url, headers=headers)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")

# Inspect the page: playlist songs are inside 'li' with class 'playlist-item' (example)
songs = []
for item in soup.select("li.playlist-item"):  # <-- you may need to adjust this selector
    title_tag = item.select_one(".song-title")  # check HTML
    artist_tag = item.select_one(".song-artist")  # check HTML
    if title_tag:
        title = title_tag.get_text(strip=True)
    else:
        title = "Unknown Title"
    if artist_tag:
        artist = artist_tag.get_text(strip=True)
    else:
        artist = "Unknown Artist"
    songs.append({"title": title, "artist": artist})

# Fallback if empty
if not songs:
    songs = [{"title": "No Song", "artist": "N/A"}]

# Build EPG XML
now = datetime.datetime.utcnow()
xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<tv>']
interval = 6  # each song 6 minutes

for i, s in enumerate(songs):
    start = now - datetime.timedelta(minutes=i*interval)
    stop = start + datetime.timedelta(minutes=interval)
    title = html.escape(s["title"])
    artist = html.escape(s["artist"])
    xml.append(f'''  <programme start="{start.strftime("%Y%m%d%H%M%S")} +0000" stop="{stop.strftime("%Y%m%d%H%M%S")} +0000" channel="Radio">
    <title lang="en">{title}</title>
    <desc>{artist}</desc>
  </programme>''')

xml.append("</tv>")

with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print("epg.xml generated successfully")
