import requests
from bs4 import BeautifulSoup
import datetime
import html

# Replace with your actual radio playlist URL
url = "https://player.listenlive.co/63371/en/songhistory"
r = requests.get(url)
data = r.json()  # JSON with song list

# Example: data['songs'] contains list of latest songs
songs = data.get("songs", [])

# Current UTC time
now = datetime.datetime.utcnow()

xml = ['<?xml version="1.0" encoding="UTF-8"?>']
xml.append('<tv generator-info-name="Radio EPG">')

# Channel info
xml.append('  <channel id="988">')
xml.append('    <display-name>988 FM</display-name>')
xml.append('    <icon src="https://raw.githubusercontent.com/SGolden58/svg/main/Logo/988.png"/>')
xml.append('  </channel>')

# Generate programme entries
for i, s in enumerate(songs):
    start = now + datetime.timedelta(minutes=i*6)  # each song 6 minutes
    stop = start + datetime.timedelta(minutes=6)
    title = html.escape(s.get("title", "Unknown Song"))
    artist = html.escape(s.get("artist", "Unknown Artist"))
    xml.append(f'''  <programme start="{start.strftime("%Y%m%d%H%M%S")} +0000" stop="{stop.strftime("%Y%m%d%H%M%S")} +0000" channel="988">
    <title lang="en">{title}</title>
    <desc>{artist}</desc>
  </programme>''')

xml.append("</tv>")

# Write to epg.xml
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print("epg.xml generated successfully!")
