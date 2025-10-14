import requests
from bs4 import BeautifulSoup
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
        time_str = cols[0].get_text(strip=True)  # e.g., "5:56"
        title_artist = cols[1].get_text(strip=True)

        # Split title and artist
        if " - " in title_artist:
            title, artist = title_artist.split(" - ", 1)
        else:
            title, artist = title_artist, ""

        songs.append({
            "time": time_str.strip(),
            "title": title.strip(),
            "artist": artist.strip()
        })

# === 3️⃣ Build XML EPG ===
xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<tv date="" generator-info-url="https://sgolden58.github.io/radio/epg.xml" '
    'source-info-url="https://sgolden58.github.io/radio/epg.xml?channel_id=988&date=">',
    '<channel id="988">',
    '<display-name lang="zh">988</display-name>',
    '<icon src=""/>',
    '</channel>'
]

# === 4️⃣ Add songs as <programme> ===
for i, s in enumerate(songs):
    start_time = s["time"]
    # Stop time = 1 second before next song start, but keep same format
    if i + 1 < len(songs):
        stop_time = songs[i + 1]["time"]
    else:
        stop_time = start_time

    # Escape special characters like &
    title_escaped = html.escape(s['title'], quote=True)
    artist_escaped = html.escape(s['artist'], quote=True)

    xml.append(f'<programme channel="988" start="{start_time}" stop="{stop_time}">')
    xml.append(f'  <title lang="zh">{title_escaped}</title>')
    xml.append(f'  <desc lang="zh">{artist_escaped}</desc>')
    xml.append(f'  <date>{start_time}</date>')
    xml.append('</programme>')

xml.append('</tv>')

# === 5️⃣ Write XML file ===
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print("✅ EPG XML successfully generated as epg.xml")
