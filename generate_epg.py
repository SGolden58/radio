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

# Limit to the latest 33 songs
songs = songs[:33]

# === 3️⃣ Prepare datetime objects ===
tz_myt = datetime.timezone(datetime.timedelta(hours=8))
now = datetime.datetime.now(tz_myt)  # this becomes your <tv date>
start_times = []

from datetime import datetime, timedelta, timezone

tz_myt = timezone(timedelta(hours=8))
today = datetime.now(tz=tz_myt).date()  # Malaysia date

start_times = []

for s in songs:
    # parse song time from the playlist
    try:
        h, m = map(int, s["time"].split(":"))
    except ValueError:
        continue
    start_dt = datetime.combine(today, datetime.time(hour=h, minute=m, tzinfo=tz_myt))
    start_times.append(start_dt)

# Prepare stop times (1 second before next song)
stop_times = []
for i in range(len(start_times)):
    if i + 1 < len(start_times):
        stop_times.append(start_times[i + 1] - timedelta(seconds=1))
    else:
        stop_times.append(start_times[i] + timedelta(minutes=3))  # last song

# Prepare stop times (1 second before next song)
stop_times = []
for i in range(len(start_times)):
    if i + 1 < len(start_times):
        stop_times.append(start_times[i + 1] - datetime.timedelta(seconds=1))
    else:
        stop_times.append(start_times[i] + datetime.timedelta(minutes=3))  # last song

from datetime import datetime, timedelta, timezone

tz_myt = timezone(timedelta(hours=8))  # Malaysia time zone

# === 4️⃣ Build XML EPG (Televizo)  ===
now = datetime.now(tz=tz_myt)

# use this 'now' as your tv_date
tv_date_str = now.strftime("%Y%m%d%H%M%S") + " +0800"
base_date = now.date()  # use this date for all programme times

xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<?xml-stylesheet type="text/xsl" href="epg.xsl"?>',  # <-- as a string
    f'<tv date="{tv_date_str}" '
    f'generator-info-url="https://sgolden58.github.io/radio/epg.xml" '
    f'source-info-url="https://sgolden58.github.io/radio/epg.xml?channel_id=988&amp;date={now.strftime("%Y%m%d")}">',
    '<channel id="988">',
    '<display-name>988</display-name>',
    '<icon src=""/>',
    '</channel>'
]

# === 5️⃣ Add programme blocks ===
for i, s in enumerate(songs):
    start_dt = start_times[i]
    stop_dt = stop_times[i]

    # AM/PM format for <date>
    ampm_time = start_dt.strftime("%-I:%M %p")  # 5:38 PM (Linux/mac) use %-I, Windows might need %#I

    xml.append(f'<programme channel="988" start="{start_dt.strftime("%Y%m%d%H%M%S")} +0800" stop="{stop_dt.strftime("%Y%m%d%H%M%S")} +0800">')
    xml.append(f'  <title>{s["title"]}</title>')
    xml.append(f'  <desc>{s["artist"]}</desc>')
    xml.append(f'  <date>{start_dt.strftime("%-I:%M %p")}</date>')
    xml.append('</programme>')

# === 6️⃣ Close XML ===
xml.append('</tv>')

# === 7️⃣ Save XML file ===
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print(f"✅ EPG.xml generated successfully — {len(songs)} songs with exact playlist times (Malaysia +0800).")
