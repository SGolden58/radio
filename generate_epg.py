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

for row in rows:
    cols = row.find_all("td")
    if len(cols) >= 2:
        time_str = cols[0].get_text(strip=True)
        title_artist = cols[1].get_text(strip=True)
        if not time_str or not title_artist:
            continue

        if " - " in title_artist:
            title, artist = title_artist.split(" - ", 1)
        else:
            title, artist = title_artist.strip(), ""

        title = title.strip()
        artist = artist.strip()

        # Only include entries with something
        if not title and not artist:
            continue

        songs.append({"time": time_str, "title": title, "artist": artist})

# Take the latest 33 songs (from bottom of list)
songs = songs[-33:]

# === 3️⃣ Prepare start times ===
tz = datetime.timezone(datetime.timedelta(hours=8))
today = datetime.datetime.now(tz).date()
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
    '</
