import requests
from bs4 import BeautifulSoup
import datetime
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
        time_str = cols[0].get_text(strip=True)  # e.g., 4:55
        artist = cols[1].get_text(strip=True)
        title = cols[2].get_text(strip=True)
        if artist and title and time_str:
            songs.append({"time_str": time_str, "artist": artist, "title": title})

# === 3️⃣ Prepare start and stop times in Malaysia timezone ===
tz = datetime.timezone(datetime.timedelta(hours=8))
today = datetime.datetime.now(tz).date()

start_times = []
for s in songs:
    h, m = map(int, s["time_str"].split(":"))
    start_dt = datetime.datetime(today.year, today.month, today.day, h, m, 0, tzinfo=tz)
    start_times.append(start_dt)

stop_times = []
for i in range(len(start_times)):
    if i + 1 < len(start_times):
        stop_times.append(start_times[i + 1] - datetime.timedelta(seconds=1))
    else:
        stop_times.append(start_times[i] + datetime.timedelta(minutes=2))  # last song

# === 4️⃣ XML header ===
now = datetime.datetime.now(tz)
xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<tv date="{now.strftime("%Y%m%d%H%M%S")} +0800" '
    f'generator-info-url="https://sgolden58.github.io/radio/epg.xml" '
    f'source-info-url="https://sgolden58.github.io/radio/epg.xml?channel_id=988&amp;date={now.strftime("%Y%m%d")}&amp;timezone=None">',
    '<channel id="988">',
    '<display-name lang="zh">988</display-name>',
    '<icon src=""/>',
    '</channel>'
]

# === 5️⃣ Add programmes ===
for i, s in enumerate(songs):
    start_dt = start_times[i]
    stop_dt = stop_times[i]

    title_escaped = html.escape(s["artist"], quote=True)
    desc_escaped = html.escape(s["title"], quote=True)

    # Keep AM/PM based on KL timezone
    ampm_time = start_dt.strftime("%I:%M %p").lstrip("0")

    xml.append(f'<programme channel="988" start="{start_dt.strftime("%Y%m%d%H%M%S")} +0800" stop="{stop_dt.strftime("%Y%m%d%H%M%S")} +0800">')
    xml.append(f'  <title lang="zh">{title_escaped}</title>')
    xml.append(f'  <desc lang="zh">{desc_escaped}</desc>')
    xml.append(f'  <date>{ampm_time}</date>')
    xml.append('</programme>')

# === 6️⃣ Close XML ===
xml.append('</tv>')

# === 7️⃣ Save XML ===
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print(f"✅ EPG.xml generated — {len(songs)} songs, times exactly as URL in Malaysia timezone")
