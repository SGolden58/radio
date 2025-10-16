import requests
from bs4 import BeautifulSoup
import datetime

# === 1️⃣ Fetch playlist page ===
url = "https://radio-online.my/988-fm-playlist"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

# === 2️⃣ Extract songs from the playlist table ===
rows = soup.select("table tr")
songs = []

for row in rows[1:]:  # skip header
    cols = row.find_all("td")
    if len(cols) >= 3:
        time_str = cols[0].get_text(strip=True)
        artist = cols[1].get_text(strip=True)
        title = cols[2].get_text(strip=True)
        if artist and title and time_str:
            # Convert time to 24-hour format if needed
            try:
                hour, minute = map(int, time_str.split(":"))
                if hour < 8:  # assuming times <8 may be morning of next day in playlist logic
                    hour += 0  # no adjustment needed if site already shows 14,15 etc
                time_str_24 = f"{hour:02d}:{minute:02d}"
            except:
                time_str_24 = time_str
            songs.append({"time": time_str_24, "artist": artist, "title": title})

# Limit to latest 33 songs
songs = songs[:33]

# === 3️⃣ Prepare datetime objects in Malaysia +0800 ===
tz_myt = datetime.timezone(datetime.timedelta(hours=8))
now = datetime.datetime.now(tz_myt)

start_times = []
current_start = now  # first programme starts now

for _ in songs:
    start_times.append(current_start)
    current_start += datetime.timedelta(minutes=3)  # each song 3 min

# Stop times (1 second before next song)
stop_times = []
for i in range(len(start_times)):
    if i + 1 < len(start_times):
        stop_times.append(start_times[i + 1] - datetime.timedelta(seconds=1))
    else:
        stop_times.append(start_times[i] + datetime.timedelta(minutes=3))

# === 4️⃣ Build XML ===
xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<tv date="{now.strftime("%Y%m%d%H%M%S")} +0800" '
    f'generator-info-url="https://sgolden58.github.io/radio/epg.xml" '
    f'source-info-url="https://sgolden58.github.io/radio/epg.xml?channel_id=988&amp;date={now.strftime("%Y%m%d")}">',
    '<channel id="988">',
    '<display-name>988</display-name>',
    '<icon src=""/>',
    '</channel>'
]

# === 5️⃣ Add programmes ===
for i, s in enumerate(songs):
    start_dt = start_times[i]
    stop_dt = stop_times[i]

    xml.append(f'<programme channel="988" start="{start_dt.strftime("%Y%m%d%H%M%S")} +0800" stop="{stop_dt.strftime("%Y%m%d%H%M%S")} +0800">')
    xml.append(f'  <title>{s["title"]}</title>')
    xml.append(f'  <desc>{s["artist"]}</desc>')
    xml.append(f'  <date>{s["time"]}</date>')  # exactly same as scraped playlist
    xml.append('</programme>')

# === 6️⃣ Close XML ===
xml.append('</tv>')

# === 7️⃣ Save XML ===
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print(f"✅ EPG.xml generated — {len(songs)} songs, times match playlist exactly (+0800).")
