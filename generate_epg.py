import requests
from bs4 import BeautifulSoup
import datetime
import html

# === 1️⃣ Fetch playlist page ===
url = "https://radio-online.my/988-fm-playlist"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

# === 2️⃣ Extract songs ===
rows = soup.select("table tr")
songs = []

for row in rows[1:]:  # skip header
    cols = row.find_all("td")
    if len(cols) >= 3:
        time_str = cols[0].get_text(strip=True)  # e.g., "5:51"
        artist = cols[1].get_text(strip=True)
        title = cols[2].get_text(strip=True)
        if artist and title and time_str:
            songs.append({"time": time_str, "artist": artist, "title": title})

# Limit to last 33 songs
songs = songs[:33]

# === 3️⃣ Build XML ===
now = datetime.datetime.now()
xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<tv date="{now.strftime("%Y%m%d%H%M%S")} +0800" generator-info-url="https://sgolden58.github.io/radio/epg.xml" source-info-url="https://sgolden58.github.io/radio/epg.xml?channel_id=988&amp;date={now.strftime("%Y%m%d")}">',
    '<channel id="988">',
    '<display-name>988</display-name>',
    '<icon src=""/>',
    '</channel>'
]

# === 4️⃣ Add programmes ===
for i in range(len(songs)):
    s = songs[i]
    start_time_str = s["time"]

    # Compute stop time as "1 second before next song", use dummy stop for last song
    if i + 1 < len(songs):
        next_time_str = songs[i + 1]["time"]
        stop_time_str = next_time_str  # for now, keep as string; we'll format later
    else:
        stop_time_str = start_time_str  # last song, arbitrary

    # Keep times exactly as in playlist, no conversion
    xml.append(f'<programme channel="988" start="{start_time_str}" stop="{stop_time_str}">')
    xml.append(f'  <title>{s["title"]}</title>')
    xml.append(f'  <desc>{s["artist"]}</desc>')
    xml.append(f'  <date>{start_time_str}</date>')
    xml.append('</programme>')

xml.append('</tv>')

# === 5️⃣ Save XML ===
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print("✅ EPG.xml generated — times exactly match playlist.")
