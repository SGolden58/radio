import requests
from bs4 import BeautifulSoup
import datetime
import html

# URL of the radio playlist
url = "https://radio-online.my/988-fm-playlist"
r = requests.get(url)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")

# Example: find table or divs with song info
# Adjust selectors according to the webpage structure
songs = []
for row in soup.select(".song-list tr"):  # Replace with actual selector
    title_tag = row.select_one(".song-title")
    artist_tag = row.select_one(".song-artist")
    time_tag = row.select_one(".song-time")  # If available

    if title_tag and artist_tag:
        songs.append({
            "title": title_tag.get_text(strip=True),
            "artist": artist_tag.get_text(strip=True),
            "time": time_tag.get_text(strip=True) if time_tag else None
        })

# Create XML
now = datetime.datetime.utcnow()
xml = [
    f'<?xml version="1.0" encoding="UTF-8"?>',
    f'<tv date="{now.strftime("%Y%m%d%H%M%S")} +0800" generator-info-url="https://radio-online.my/988-fm-playlist" source-info-url="{url}">',
    '<channel id="988"></channel>'
]

for s in songs:
    # If the playlist has a timestamp, parse it; otherwise, use 10-min intervals
    start = now
    stop = start + datetime.timedelta(minutes=10)
    title = html.escape(s.get("title", "Unknown"))
    artist = html.escape(s.get("artist", "Unknown"))

    xml.append(f'''<programme channel="988" start="{start.strftime("%Y%m%d%H%M%S")} +0000" stop="{stop.strftime("%Y%m%d%H%M%S")} +0000">
  <title lang="zh">{title}</title>
  <desc>{artist}</desc>
  <date>{now.strftime("%Y-%m-%d")}</date>
</programme>''')

    now = stop  # next start = previous stop

xml.append("</tv>")

with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))
