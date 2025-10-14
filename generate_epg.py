import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
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
        time_str = cols[0].get_text(strip=True)  # e.g., 5:53
        artist = cols[1].get_text(strip=True)
        title = cols[2].get_text(strip=True)
        if time_str and artist and title:
            # Parse hour/minute and determine AM/PM
            hour, minute = map(int, time_str.split(":"))
            ampm = "am" if hour < 12 else "pm"
            songs.append({
                "hour": hour,
                "minute": minute,
                "artist": artist,
                "title": title,
                "ampm": ampm,
                "time_str": time_str
            })

# === Build XML ===
now = datetime.now()
date_only = now.strftime("%Y%m%d")
tv_date = now.strftime("%Y%m%d%H%M%S")

xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<tv date="{tv_date}" '
    f'generator-info-url="https://sgolden58.github.io/radio/epg.xml" '
    f'source-info-url="https://sgolden58.github.io/radio/epg.xml?channel_id=988&amp;date={date_only}&amp;timezone=None">',
    '<channel id="988">',
    '<display-name lang="zh">988</display-name>',
    '<icon src=""/>',
    '</channel>'
]

for i, song in enumerate(songs):
    # Start datetime for this song
    start_dt = now.replace(hour=song["hour"], minute=song["minute"], second=0, microsecond=0)
    
    # Stop time: 1 second before next song, or +5 mins if last
    if i + 1 < len(songs):
        next_song = songs[i + 1]
        stop_dt = now.replace(hour=next_song["hour"], minute=next_song["minute"], second=0, microsecond=0) - timedelta(seconds=1)
    else:
        stop_dt = start_dt + timedelta(minutes=5)

    xml.append(f'<programme channel="988" start="{start_dt.strftime("%Y%m%d%H%M%S")}" stop="{stop_dt.strftime("%Y%m%d%H%M%S")}">')
    xml.append(f'  <title lang="zh">{html.escape(song["artist"])}</title>')
    xml.append(f'  <desc lang="zh">{html.escape(song["title"])}</desc>')
    xml.append(f'  <date>{song["time_str"]} {song["ampm"]}</date>')
    xml.append('</programme>')

xml.append('</tv>')

with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print(f"✅ EPG.xml generated — {len(songs)} songs, times follow URL exactly")
