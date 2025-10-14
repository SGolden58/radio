import requests
from bs4 import BeautifulSoup
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
        time_str = cols[0].get_text(strip=True)  # e.g., 5:56
        title_artist = cols[1].get_text(strip=True)

        if " - " in title_artist:
            title, artist = title_artist.split(" - ", 1)
        else:
            title, artist = title_artist, ""

        songs.append({
            "time": time_str,      # keep as-is
            "title": title.strip(),
            "artist": artist.strip()
        })

# === 3️⃣ Build XML EPG ===
xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<tv date="" generator-info-url="https://sgolden58.github.io/radio/epg.xml" '
    f'source-info-url="https://sgolden58.github.io/radio/epg.xml?channel_id=988&date=">',
    '<channel id="9
