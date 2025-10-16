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
            songs.append({"time": time_str, "artist": artist, "title": title})

# Limit to latest 33 songs
songs = songs[:33]

# === 3️⃣ Convert playlist times to datetime objects (Malaysia +0800) ===
tz_myt = datetime.timezone(datetime.timedelta(hours=8))
program_times = []
for s in songs:
    hour, minute = map(int, s["time"].split(":"))
    dt = datetime.datetime(
        year=datetime.datetime.now().year,
        month=datetime.datetime.now().month,
        day=datetime.datetime.now().day,
        hour=hour,
        minute=minute,
        second=0,
        tzinfo=tz_myt
    )
    program_times.append(dt)

# === 4️⃣ Build stop times (1 sec before next song) ===
stop_times = []
for i in range(len(program_times)):
    if i + 1 < len(program_times):
        stop_times.append(program_times[i + 1] - datetime.timedelta(seconds=1))
    else:
        stop_times.append(program_times[i] + datetime.timedelta(minutes=3))  # last song

# === 5️⃣ Build XML ===
now = datetime.datetime.now(tz_myt)
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

# === 6️⃣ Add programme blocks ===
for i, s in enumerate(songs):
    start_dt = program_times[i]
    stop_dt = stop_times[i]

    xml.append(f'<programme channel="988" start="{start_dt.strftime("%Y%m%d%H%M%S")} +0800" stop="{stop_dt.strftime("%Y%m%d%H%M%S")} +0800">')
    xml.append(f'  <title>{s["title"]}</title>')
    xml.append(f'  <desc>{s["artist"]}</desc>')
    xml.append(f'  <date>{s["time"]}</date>')  # exactly as playlist
    xml.append('</programme>')

# === 7️⃣ Close XML ===
xml.append('</tv>')

# === 8️⃣ Save XML ===
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print(f"✅ EPG.xml generated — {len(songs)} songs, times exactly match playlist.")
