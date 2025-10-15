import requests
from bs4 import BeautifulSoup
import datetime

# Fetch playlist
url = "https://radio-online.my/988-fm-playlist"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

# Extract songs
rows = soup.select("table tr")
songs = []
for row in rows[1:]:
    cols = row.find_all("td")
    if len(cols) >= 3:
        time_str = cols[0].get_text(strip=True)
        artist = cols[1].get_text(strip=True)
        title = cols[2].get_text(strip=True)
        if artist and title and time_str:
            songs.append({"time": time_str, "artist": artist, "title": title})

# Take latest 33 songs
songs = songs[:33]

# Prepare start/stop times
tz_myt = datetime.timezone(datetime.timedelta(hours=8))
today = datetime.datetime.now(tz_myt).date()
start_times = []

for s in songs:
    h, m = map(int, s["time"].split(":"))
    dt = datetime.datetime(today.year, today.month, today.day, h, m, 0, tzinfo=tz_myt)
    start_times.append(dt)

# If playlist crosses midnight
for i in range(1, len(start_times)):
    if start_times[i] < start_times[i-1]:
        start_times[i] += datetime.timedelta(days=1)

stop_times = []
for i in range(len(start_times)):
    if i + 1 < len(start_times):
        stop_times.append(start_times[i+1] - datetime.timedelta(seconds=1))
    else:
        stop_times.append(start_times[i] + datetime.timedelta(minutes=3))  # last song guess

# Build XML
now = datetime.datetime.now(tz_myt)
xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<tv date="{now.strftime("%Y%m%d%H%M%S")} +0800" generator-info-url="https://sgolden58.github.io/radio/epg.xml" source-info-url="https://sgolden58.github.io/radio/epg.xml?channel_id=988&amp;date={now.strftime("%Y%m%d")}">',
    '<channel id="988">',
    '<display-name>988</display-name>',
    '<icon src=""/>',
    '</channel>'
]

# Add programmes with correct Malaysia AM/PM time
for i, s in enumerate(songs):
    start_dt = start_times[i]
    stop_dt = stop_times[i]

    ampm_time = start_dt.strftime("%-I:%M %p")  # 12-hour format, Malaysia local

    xml.append(f'<programme channel="988" start="{start_dt.strftime("%Y%m%d%H%M%S")} +0800" stop="{stop_dt.strftime("%Y%m%d%H%M%S")} +0800">')
    xml.append(f'  <title>{s["title"]}</title>')
    xml.append(f'  <desc>{s["artist"]}</desc>')
    xml.append(f'  <date>{ampm_time}</date>')
    xml.append('</programme>')

xml.append('</tv>')

with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print(f"✅ EPG.xml generated with exact Malaysia playlist times.")
