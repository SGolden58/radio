import requests
from bs4 import BeautifulSoup
import datetime
import html

# URL for latest songs
url = "https://player.listenlive.co/63371/en/songhistory"
r = requests.get(url)

songs = []

# Try JSON first
try:
    data = r.json()
    songs = data.get("songs", [])
except:
    # Fallback: parse HTML if JSON fails
    soup = BeautifulSoup(r.text, "html.parser")
    # Example: find song info in HTML (adjust selectors)
    for item in soup.select(".song-item"):  # <- adjust based on actual site
        title = item.select_one(".title").get_text(strip=True)
        artist = item.select_one(".artist").get_text(strip=True)
        songs.append({"title": title, "artist": artist})

if not songs:
    # Fallback: placeholder songs if nothing found
    songs = [{"title": f"Song {i+1}", "artist": "Unknown"} for i in range(10)]

# Current UTC time
now = datetime.datetime.utcnow()

xml = ['<?xml version="1.0" encoding="UTF-8"?>']
xml.append('<tv generator-info-name="Radio EPG">')

# Channel info
xml.append('  <channel id="988">')
xml.append('    <display-name>988 FM</display-name>')
xml.append('    <icon src="https://raw.githubusercontent.com/SGolden58/svg/main/Logo/988.png"/>')
xml.append('  </channel>')

# Generate programme entries (6 minutes per song)
for i, s in enumerate(songs):
    start = now + datetime.timedelta(minutes=i*6)
    stop = start + datetime.timedelta(minutes=6)
    title = html.escape(s.get("title", "Unknown Song"))
    artist = html.escape(s.get("artist", "Unknown Artist"))
    xml.append(f'''  <programme start="{start.strftime("%Y%m%d%H%M%S")} +0000" stop="{stop.strftime("%Y%m%d%H%M%S")} +0000" channel="988">
    <title lang="en">{title}</title>
    <desc>{artist}</desc>
  </programme>''')

xml.append("</tv>")

with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print("epg.xml generated successfully!")
