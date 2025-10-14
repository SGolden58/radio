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

        # Split into title + artist
        if " - " in title_artist:
            title, artist = title_artist.split(" - ", 1)
            title, artist = title.strip(), artist.strip()
        else:
            title, artist = title_artist.strip(), ""

        songs.append({"time": time_str, "title": title, "artist": artist})

# Keep latest 60 only
songs = songs[:60]

# === 3️⃣ Malaysia timezone ===
tz = datetime.timezone(datetime.timedelta(hours=8))
now = datetime.datetime.now(tz)
today = now.date()

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
xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<tv date="{now.strftime("%Y%m%d%H%M%S")} +0800" '
    'generator-info-url="https://sgolden58.github.io/radio/epg.xml" '
    f'source-info-
