import requests
from bs4 import BeautifulSoup
import datetime
import html

# === 1️⃣ Fetch playlist page ===
url = "https://radio-online.my/988-fm-playlist"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

# === 2️⃣ Extract songs from table ===
songs_html = soup.select("table tr")
songs = []

for row in songs_html[1:]:  # skip header
    cols = row.find_all("td")
    if len(cols) >= 2:
        time_str = cols[0].get_text(strip=True)
        title_artist = cols[1].get_text(strip=True)

        if " - " in title_artist:
            title, artist = title_artist.split(" - ", 1)
            title, artist = title.strip(), artist.strip()
        else:
            title, artist = title_artist.strip(), ""

        songs.append({"time": time_str, "title": title, "artist": artist})

# Keep latest 60 songs
songs = songs[:60]

# === 3️⃣ Malaysia timezone ===
tz = datetime.timezone(datetime.timedelta(hours=8))
today = datetime.datetime.now(tz).date()

# Parse start times
start_times = []
for s in songs:
    try:
        h, m = map(int, s["time"].split(":"))
        dt = datetime.datetime(today.year, today.month, today.day, h, m, 0, tzinfo=tz)
        start_times.append(dt)
    except Exception:
        start_times.append(None)

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

# === 5️⃣ Add programme entries ===
for i, s in enumerate(songs):
    start_dt = start_times[i]
    if not start_dt:
        continue

    # Stop time = 1 second before next song
    if i + 1 < len(start_times) and start_times[i + 1]:
        stop_dt = start_times[i + 1] - datetime.timedelta(seconds=1)
    else:
        # If last song, just +2 minutes (arbitrary, won't matter)
        stop_dt = start_dt + datetime.timedelta(minutes=2)

    artist = s["artist"].strip()
    title = s["title"].strip()

    # Remove duplicates like "杨丞琳 - 杨丞琳"
    if artist == title:
        title = ""

    if artist and title:
        display = f"{artist} - {title}"
    else:
        display = artist or title  # show whichever exists

    display_escaped = html.escape(display, quote=True)

    xml.append(f'<programme channel="988" start="{start_dt.strftime("%Y%m%d%H%M%S")} +0800" stop="{stop_dt.strftime("%Y%m%d%H%M%S")} +0800">')
    xml.append(f'  <title lang="zh">{display_escaped}</title>')
    xml.append(f'  <desc lang="zh">{display_escaped}</desc>')
    xml.append(f'  <date>{s["time"]}</date>')
    xml.append('</programme>')

xml.append('</tv>')

# === 6️⃣ Save XML ===
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print("✅ EPG.xml generated successfully — accurate start times, clean display")
