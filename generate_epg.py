import requests
from bs4 import BeautifulSoup
import html

# === Fetch playlist page ===
url = "https://radio-online.my/988-fm-playlist"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

# === Extract songs ===
rows = soup.select("table tr")
songs = []

for row in rows[1:]:
    cols = row.find_all("td")
    if len(cols) >= 3:
        time_str = cols[0].get_text(strip=True)  # e.g., 6:00
        artist = cols[1].get_text(strip=True)
        title = cols[2].get_text(strip=True)
        if time_str and artist and title:
            # Determine AM/PM based on hour
            hour = int(time_str.split(":")[0])
            ampm = "am" if hour < 12 else "pm"
            # Keep time exactly as URL
            songs.append({
                "time": time_str,
                "artist": artist,
                "title": title,
                "ampm": ampm
            })

# === Build XML ===
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
    # stop time = 1 second before next song start if exists, else same as start
    if i + 1 < len(songs):
        stop_time = songs[i + 1]["time"]
    else:
        stop_time = start_time
    xml.append(f'<programme channel="988" start="{start_time}" stop="{stop_time}">')
    xml.append(f'  <title lang="zh">{html.escape(song["artist"])}</title>')
    xml.append(f'  <desc lang="zh">{html.escape(song["title"])}</desc>')
    xml.append(f'  <date>{song["time"]} {song["ampm"]}</date>')
    xml.append('</programme>')

xml.append('</tv>')

with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print(f"✅ EPG.xml generated — {len(songs)} songs, times exactly as URL with AM/PM")
