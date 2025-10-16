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
            # Convert scraped time to 24-hour Malaysia time
            try:
                hour, minute = map(int, time_str.split(":"))
                # If hour < 8, assume site is showing UTC, add 8
                hour = (hour + 8) % 24
                time_str_24 = f"{hour:02d}:{minute:02d}"
            except:
                time_str_24 = time_str
            songs.append({"time": time_str_24, "artist": artist, "title": title})

# Limit to latest 33 songs
songs = songs[:33]

# === 3️⃣ Prepare datetime objects in UTC ===
now_malaysia = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
start_times_utc = []
current_start = now_malaysia.astimezone(datetime.timezone.utc)  # convert to UTC

for _ in songs:
    start_times_utc.append(current_start)
    current_start += datetime.timedelta(minutes=3)  # each song 3 min

# Prepare stop times (1 second before next)
stop_times_utc = []
for i in range(len(start_times_utc)):
    if i + 1 < len(start_times_utc):
        stop_times_utc.append(start_times_utc[i + 1] - datetime.timedelta(seconds=1))
    else:
        stop_times_utc.append(start_times_utc[i] + datetime.timedelta(minutes=3))

# === 4️⃣ Build XML EPG ===
xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<tv date="{now_malaysia.strftime("%Y%m%d%H%M%S")} +0800" '
    f'generator-info-url="https://sgolden58.github.io/radio/epg.xml" '
    f'source-info-url="https://sgolden58.github.io/radio/epg.xml?channel_id=988&amp;date={now_malaysia.strftime("%Y%m%d")}">',
    '<channel id="988">',
    '<display-name>988</display-name>',
    '<icon src=""/>',
    '</channel>'
]

# === 5️⃣ Add programme blocks ===
for i, s in enumerate(songs):
    start_dt = start_times_utc[i]
    stop_dt = stop_times_utc[i]

    xml.append(f'<programme channel="988" start="{start_dt.strftime("%Y%m%d%H%M%S")} +0000" stop="{stop_dt.strftime("%Y%m%d%H%M%S")} +0000">')
    xml.append(f'  <title>{s["title"]}</title>')
    xml.append(f'  <desc>{s["artist"]}</desc>')
    xml.append(f'  <date>{s["time"]}</date>')  # exact number from playlist
    xml.append('</programme>')

# === 6️⃣ Close XML ===
xml.append('</tv>')

# === 7️⃣ Save XML file ===
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print(f"✅ EPG.xml generated — {len(songs)} songs, times match playlist exactly.")
