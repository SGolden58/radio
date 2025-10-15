import requests
from bs4 import BeautifulSoup
import datetime
import html

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
today = datetime.datetime.now(tz_myt).date()
start_times = []

for s in songs:
    try:
        h, m = map(int, s["time"].split(":"))
    except ValueError:
        continue
    dt_local = datetime.datetime(today.year, today.month, today.day, h, m, 0, tzinfo=tz_myt)
    start_times.append(dt_local)

# if playlist crosses midnight, adjust dates
for i in range(1, len(start_times)):
    if start_times[i] < start_times[i - 1]:
        start_times[i] += datetime.timedelta(days=1)

stop_times = []
for i in range(len(start_times)):
    if i + 1 < len(start_times):
        stop_times.append(start_times[i + 1] - datetime.timedelta(seconds=1))
    else:
        stop_times.append(start_times[i] + datetime.timedelta(minutes=3))  # last song duration guess

# === 4️⃣ Build XML header ===
now_utc = datetime.datetime.now(datetime.timezone.utc)
xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<tv date="{now_utc.strftime("%Y%m%d%H%M%S")} +0000" '
    f'generator-info-url="https://sgolden58.github.io/radio/epg.xml" '
    f'source-info-url="https://sgolden58.github.io/radio/epg.xml?channel_id=988&amp;date={now_utc.strftime("%Y%m%d")}">',
    '  <channel id="988">',
    '    <display-name>988</display-name>',
    '    <icon src=""/>',
    '  </channel>'
]

# === 5️⃣ Add programme blocks ===
for i, s in enumerate(songs):
    if i >= len(start_times) or i >= len(stop_times):
        continue

    start_dt_utc = start_times[i].astimezone(datetime.timezone.utc)
    stop_dt_utc = stop_times[i].astimezone(datetime.timezone.utc)

    artist_escaped = html.escape(s["artist"], quote=True)
    title_escaped = html.escape(s["title"], quote=True)

    xml.append(
        f'  <programme channel="988" start="{start_dt_utc.strftime("%Y%m%d%H%M%S")} +0000" '
        f'stop="{stop_dt_utc.strftime("%Y%m%d%H%M%S")} +0000">'
    )
    xml.append(f'    <title>{artist_escaped}</title>')
    xml.append(f'    <desc>{title_escaped}</desc>')
    xml.append(f'    <date>{s["time"]}</date>')
    xml.append('  </programme>')

# === 6️⃣ Close XML ===
xml.append('</tv>')

# === 7️⃣ Save XML file ===
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print(f"✅ EPG.xml generated successfully — {len(songs)} songs found and converted to UTC time.")
