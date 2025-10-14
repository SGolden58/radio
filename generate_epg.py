import requests
from bs4 import BeautifulSoup
import datetime
import html

# === 1️⃣ Fetch playlist page ===
url = "https://radio-online.my/988-fm-playlist"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

# === 2️⃣ Extract songs from table ===
# Using a more flexible selector to handle <tbody> if present
rows = soup.select("table tr")
songs = []

for row in rows:
    cols = row.find_all("td")
    if len(cols) >= 2:
        time_str = cols[0].get_text(strip=True)
        title_artist = cols[1].get_text(strip=True)

        if not time_str or not title_artist:
            continue

        # Split artist and title
        if " - " in title_artist:
            title, artist = title_artist.split(" - ", 1)
        else:
            title, artist = title_artist.strip(), ""

        title = title.strip()
        artist = artist.strip()

        songs.append({
            "time": time_str,  # Use the exact time from the site
            "title": title,
            "artist": artist
        })

# Keep latest 60 songs
songs = songs[:60]

# === 3️⃣ Malaysia timezone ===
tz = datetime.timezone(datetime.timedelta(hours=8))
today = datetime.datetime.now(tz).date()

# === 4️⃣ Parse start times ===
start_times = []
for s in songs:
    try:
        h, m = map(int, s["time"].split(":"))
        dt = datetime.datetime(today.year, today.month, today.day, h, m, 0, tzinfo=tz)
        start_times.append(dt)
    except Exception:
        start_times.append(None)

# === 5️⃣ Build XML header ===
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

# === 6️⃣ Add programme entries ===
for i, s in enumerate(songs):
    start_dt = start_times[i]
    if not start_dt:
        continue

    # Stop = 1 second before next song
    if i + 1 < len(start_times) and start_times[i + 1]:
        stop_dt = start_times[i + 1] - datetime.timedelta(seconds=1)
    else:
        stop_dt = start_dt + datetime.timedelta(minutes=2)

    artist = s["artist"]
    title = s["title"]

    # Fix identical artist/title
    if artist == title:
        display_title = artist
        # Fallback desc = next song title if exists
        display_desc = songs[i + 1]["title"] if i + 1 < len(songs) else artist
    else:
        display_title = artist or title
        display_desc = title or artist

    # Escape XML
    title_escaped = html.escape(display_title, quote=True)
    desc_escaped = html.escape(display_desc, quote=True)

    xml.append(f'<programme channel="988" start="{start_dt.strftime("%Y%m%d%H%M%S")} +0800" stop="{sto_
