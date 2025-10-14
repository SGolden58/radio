import requests
from bs4 import BeautifulSoup
import datetime
import html

# URL of your radio song history
url = "https://player.listenlive.co/63371/en/songhistory"
r = requests.get(url)
r.raise_for_status()  # fail if request fails

# Try JSON first
try:
    songs = r.json().get("songs", [])
except Exception:
    # fallback: parse HTML if not JSON
    soup = BeautifulSoup(r.text, "html.parser")
    songs = []
    for item in soup.select(".song"):  # update selector to match page
        title = item.get_text(strip=True)
        songs.append({"title": title, "artist": "Unknown Artist"})

if not songs:
    songs = [{"title": "No Song", "artist": "N/A"}]

# Current UTC time
now = datetime.datetime.utcnow()

# Build XML
xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<tv>']

# Each song per 6 minutes (adjust as needed)
interval = 6
for i, s in enumerate(songs):
    start = now - datetime.timedelta(minutes=i*interval)
    stop = start + datetime.timedelta(minutes=interval)
    title = html.escape(s.get("title", "Unknown Song"))
    artist = html.escape(s.get("artist", "Unknown Artist"))
    xml.append(f'''  <programme start="{start.strftime("%Y%m%d%H%M%S")} +0000" stop="{stop.strftime("%Y%m%d%H%M%S")} +0000" channel="Radio">
    <title lang="en">{title}</title>
    <desc>{artist}</desc>
  </programme>''')

xml.append("</tv>")

with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print("epg.xml generated successfully")
