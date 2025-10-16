import requests
from bs4 import BeautifulSoup
import datetime

# === 1️⃣ Fetch playlist page ===
url = "https://online-radio.my/12-988-fm.html"
r = requests.get(url)
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")

# === 2️⃣ Find the correct playlist table ===
# The playlist table has class "table" and is inside a div with id "playlist" (based on page inspection)
playlist_div = soup.find("div", id="playlist")
if not playlist_div:
    raise RuntimeError("Playlist div not found on page")

table = playlist_div.find("table")
if not table:
    raise RuntimeError("Playlist table not found inside playlist div")

rows = table.find_all("tr")

songs = []

# === 3️⃣ Extract songs from the playlist table ===
# Inspecting the page shows columns: Time | Artist | Title (3 columns)
for row in rows[1:]:  # skip header row
    cols = row.find_all("td")
    if len(cols) >= 3:
        time_str = cols[0].get_text(strip=True)
        artist = cols[1].get_text(strip=True)
        title = cols[2].get_text(strip=True)
        if time_str and artist and title:
            songs.append({"time": time_str, "artist": artist, "title": title})

if not songs:
    raise RuntimeError("No songs found in playlist table")

# Limit to the latest 10 songs
songs = songs[:10]

# === 4️⃣ Prepare datetime objects ===
tz_myt = datetime.timezone(datetime.timedelta(hours=8))
now = datetime.datetime.now(tz_myt)

start_times = []
current_start = now

for _ in songs:
    start_times.append(current_start)
    current_start += datetime.timedelta(minutes=3)  # each song = 3 min

stop_times = []
for i in range(len(start_times)):
    if i + 1 < len(start_times):
        stop_times.append(start_times[i + 1] - datetime.timedelta(seconds=1))
    else:
        stop_times.append(start_times[i] + datetime.timedelta(minutes=3))

# === 5️⃣ Build XML EPG (Televizo format) ===
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

for i, s in enumerate(songs):
    start_dt = start_times[i]
    stop_dt = stop_times[i]

    # For Windows compatibility in strftime use %#I instead of %-I if needed
    try:
        ampm_time = start_dt.strftime("%-I:%M %p")  # Linux/macOS
    except ValueError:
        ampm_time = start_dt.strftime("%#I:%M %p")  # Windows fallback

    xml.append(f'<programme channel="988" start="{start_dt.strftime("%Y%m%d%H%M%S")} +0800" stop="{stop_dt.strftime("%Y%m%d%H%M%S")} +0800">')
    xml.append(f'  <title>{s["title"]} + {s["artist"]}</title>')
    xml.append(f'  <desc>{s["artist"]}</desc>')
    xml.append(f'  <date>{ampm_time}</date>')
    xml.append('</programme>')

xml.append('</tv>')

# === 6️⃣ Save XML file ===
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print(f"✅ EPG.xml generated successfully — {len(songs)} songs with exact playlist times (Malaysia +0800).")
