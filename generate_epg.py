import requests
from bs4 import BeautifulSoup
import html

# === 1️⃣ Fetch playlist page ===
url = "https://radio-online.my/988-fm-playlist"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

# === 2️⃣ Extract songs from table ===
rows = soup.select("table tr")
songs = []

for row in rows[1:]:  # skip header
    cols = row.find_all("td")
    if len(cols) >= 3:
        time_str = cols[0].get_text(strip=True)
        artist = cols[1].get_text(strip=True)
        title = cols[2].get_text(strip=True)
        if artist and title and time_str:
            songs.append({"time": time_str, "artist": artist, "title": title})

# === 3️⃣ Build XML ===
xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<tv>',
    '<channel id="988">',
    '<display-name lang="zh">988</display-name>',
    '<icon src=""/>',
    '</channel>'
]

for i, song in enumerate(songs):
    start_time = song["time"]
    if i + 1 < len(songs):
        stop_time = songs[i + 1]["time"]
    else:
        stop_time = start_time  # last song same start as stop

    xml.append(f'<programme channel="988" start="{start_time}" stop="{stop_time}">')
    xml.append(f'  <title lang="zh">{html.escape(song["artist"])}</title>')
    xml.append(f'  <desc lang="zh">{html.escape(song["title"])}</desc>')
    xml.append(f'  <date>{start_time}</date>')
    xml.append('</programme>')

xml.append('</tv>')

# === 4️⃣ Save XML ===
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print(f"✅ EPG.xml generated — {len(songs)} songs, times exactly as URL")
