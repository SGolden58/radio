import requests
from bs4 import BeautifulSoup
import datetime
import html

# Your original URL
url = "https://radio-online.my/988-fm-playlist"

headers = {"User-Agent": "Mozilla/5.0"}
r = requests.get(url, headers=headers)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")

# Update these selectors based on actual HTML of the page
songs = []
for item in soup.select("li.playlist-item"):  # Replace if needed
    title_tag = item.select_one(".song-title")  # Replace with actual class
    artist_tag = item.select_one(".song-artist")  # Replace with actual class
    title = title_tag.get_text(strip=True) if title_tag else "Unknown Title"
    artist = artist_tag.get_text(strip=True) if artist_tag else "Unknown Artist"
    songs.append({"title": title, "artist": artist})

if not songs:
    songs = [{"title": "No Song", "artist": "N/A"}]

now = datetime.datetime.utcnow()
xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<tv>']

interval = 6  # each song 6 minutes

for i, s in enumerate(songs):
    start = now - datetime.timedelta(minutes=i*interval)
    stop = start + datetime.timedelta(minutes=interval)
    xml.append(f'''  <programme start="{start.strftime("%Y%m%d%H%M%S")} +0000" stop="{stop.strftime("%Y%m%d%H%M%S")} +0000" channel="Radio">
    <title lang="en">{html.escape(s["title"])}</title>
    <desc>{html.escape(s["artist"])}</desc>
  </programme>''')

xml.append("</tv>")

with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print("epg.xml generated successfully")
