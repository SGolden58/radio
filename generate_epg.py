import requests
from bs4 import BeautifulSoup
import datetime
import html

# === 1️⃣ Fetch playlist page ===
url = "https://radio-online.my/988-fm-playlist"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

# === 2️⃣ Extract songs from table ===
songs_html = soup.select("table tr")
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

# Limit to latest 60 songs
songs = songs[:60]

# === 3️⃣ Build XML EPG ===
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))  # Malaysia time

xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<tv date="{now.strftime("%Y%m%d%H%M%S")} +0800" '
    f'generator-info-url="https://sgolden58.github.io/radio/epg.xml" '
    f'source-info-url="https://sgolden58.github.io/radio/epg.xml?channel_id=988&amp;date={now.strftime("%Y%m%d")}&amp;timezone=None">',
    '<channel id="988">',
    '<display-name lang="Malaysia">988</display-name>',
    '<icon src=""/>',
    '</channel>'
]

# === 4️⃣ Add each song as a <programme> ===
for s in songs:
    try:
        h, m = map(int, s["time"].split(":"))
        start = now.replace(hour=h, minute=m, second=0, microsecond=0)
        stop = start + datetime.timedelta(minutes=10)
    except ValueError:
        continue

    # Escape special characters safely
    title_escaped = html.escape(s['title'], quote=True)
    artist_escaped = html.escape(s['artist'], quote=True)

    xml.append(f'''<programme channel="988" start="{start.strftime("%Y%m%d%H%M%S")} +0000" stop="{stop.strftime("%Y%m%d%H%M%S")} +0000">
    <title lang="zh">{title_escaped}</title>
    <desc>{artist_escaped}</desc>
    <date>{s["time"]}</date>
</programme>''')

xml.append("</tv>")

# === 5️⃣ Write XML file ===
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print("✅ EPG XML successfully generated as epg.xml")
