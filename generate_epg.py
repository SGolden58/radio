import requests
from bs4 import BeautifulSoup
import datetime
import html

# URL to fetch the playlist
url = "https://radio-online.my/988-fm-playlist"
r = requests.get(url)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")

# Select the songs from the table
songs_html = soup.select("table tr")  # Adjust selector as needed
songs = []

for row in songs_html[1:]:  # Skip header
    cols = row.find_all("td")
    if len(cols) >= 2:
        time_str = cols[0].get_text(strip=True)
        title_artist = cols[1].get_text(strip=True)
        if " - " in title_artist:
            title, artist = title_artist.split(" - ", 1)
        else:
            title, artist = title_artist, "Unknown"  # Default to "Unknown" if no artist
        songs.append({
            "time": time_str,
            "title": songs,
            "artist": artist
        })

# Limit to the latest 60 songs
songs = songs[:60]

# Build XML
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))  # Malaysia Time
xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<tv date="{now.strftime("%Y%m%d%H%M%S")} +0800" '
    f'generator-info-url="https://sgolden58.github.io/radio/epg.xml" '
    f'source-info-url="https://sgolden58.github.io/radio/epg.xml?channel_id=988%ampdate={now.strftime("%Y%m%d")}&amptimezone=None">',
    '<channel id="988">',
    '<display-name lang="Malaysia">988</display-name>',
    '<icon src=""/>',
    '</channel>'
]

# Add each song as a programme
for s in songs:
    try:
        h, m = map(int, s["time"].split(":"))
        start = now.replace(hour=h, minute=m, second=0, microsecond=0)
        stop = start + datetime.timedelta(minutes=10)  # 10 min per song
    except ValueError:
        continue  # Skip if time parsing fails

    # Escape title and artist names to handle special characters
    title_escaped = html.escape(s['title']).replace('&', '&amp;')
    artist_escaped = html.escape(s['artist']).replace('&', '&amp;')

    # Format title and description as per your requirement
    formatted_title = f"{title_escaped}(songs)"
    formatted_desc = f"{artist_escaped}(artist)"

    xml.append(f'''<programme channel="988" start="{start.strftime("%Y%m%d%H%M%S")} +0000" stop="{stop.strftime("%Y%m%d%H%M%S")} +0000">
    <title lang="zh">{formatted_title}</title>
    <desc>{formatted_desc}</desc>
    <date>{s["time"]}</date>
</programme>''')

xml.append("</tv>")

# Write to epg.xml
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))
