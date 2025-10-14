import requests
from bs4 import BeautifulSoup
import datetime
import html

url = "https://radio-online.my/988-fm-playlist"
r = requests.get(url)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")

# The page has a table or div with songs. Adjust selector as needed
songs_html = soup.select("table tr")  # example: table rows
songs = []

for row in songs_html[1:]:  # skip header
    cols = row.find_all("td")
    if len(cols) >= 2:
        time_str = cols[0].get_text(strip=True)
        title_artist = cols[1].get_text(strip=True)
        if " - " in title_artist:
            title, artist = title_artist.split(" - ", 1)
        else:
            title, artist = title_artist, "Unknown"
        songs.append({
            "time": time_str,
            "title": title,
            "artist": artist
        })

# Build XML
xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<tv>']

for s in songs:
    # Parse time string, assuming format HH:MM
    try:
        now = datetime.datetime.utcnow()
        h, m = map(int, s["time"].split(":"))
        start = now.replace(hour=h, minute=m, second=0, microsecond=0)
        stop = start + datetime.timedelta(minutes=10)  # 10 min per song
    except:
        start = datetime.datetime.utcnow()
        stop = start + datetime.timedelta(minutes=10)

    xml.append(f'''  <programme start="{start.strftime("%Y%m%d%H%M%S")} +0000" stop="{stop.strftime("%Y%m%d%H%M%S")} +0000" channel="Radio">
    <title lang="en">{html.escape(s['title'])}</title>
    <desc>{html.escape(s['artist'])}</desc>
  </programme>''')

xml.append("</tv>")

with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))
