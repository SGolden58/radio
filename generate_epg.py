import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import xml.sax.saxutils as saxutils  # ✅ use this to escape & < >

url = "https://radio-online.my/988-fm-playlist"
res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

rows = soup.select("table tbody tr")

songs = []
for row in rows:
    cols = [c.text.strip() for c in row.find_all("td")]
    if len(cols) >= 3:
        time_str, artist, title = cols[:3]
        songs.append((time_str, artist, title))

# Only take first 10
songs = songs[:10]

xml = '<?xml version="1.0" encoding="UTF-8"?>\n<tv generator-info-name="Radio EPG Script">\n'
xml += '  <channel id="988"><display-name>988 FM</display-name></channel>\n'

now = datetime.now().replace(second=0, microsecond=0)
for i, (time_str, artist, title) in enumerate(songs):
    start = now + timedelta(minutes=i * 5)
    stop = start + timedelta(minutes=5)

    # ✅ Properly escape dangerous characters like & < >
    artist = saxutils.escape(artist)
    title = saxutils.escape(title)

    xml += f'  <programme start="{start.strftime("%Y%m%d%H%M%S")} +0800" stop="{stop.strftime("%Y%m%d%H%M%S")} +0800" channel="988">\n'
    xml += f'    <title lang="en">{title}</title>\n'
    xml += f'    <desc>{artist}</desc>\n'
    xml += '  </programme>\n'

xml += '</tv>\n'

with open("epg.xml", "w", encoding="utf-8") as f:
    f.write(xml)
    
