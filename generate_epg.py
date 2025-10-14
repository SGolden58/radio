import requests
from bs4 import BeautifulSoup
import html

url = "https://radio-online.my/988-fm-playlist"
r = requests.get(url)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")

# The site has a table or list with song times, title, and artist
# This may need adjusting if the site's HTML changes
epg_entries = []

for row in soup.select("table tbody tr"):  # adjust selector based on actual page
    try:
        time_cell = row.select_one("td.time").get_text(strip=True)
        title_cell = row.select_one("td.song").get_text(strip=True)
        artist_cell = row.select_one("td.artist").get_text(strip=True)
        
        epg_entries.append({
            "start": time_cell,
            "title": html.escape(title_cell),
            "artist": html.escape(artist_cell)
        })
    except AttributeError:
        continue

# Generate XML
xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<tv>']

for i, e in enumerate(epg_entries):
    start = e["start"]  # directly from page, format might need adjustment
    # if end time not provided, assume next song start or +5 min
    if i+1 < len(epg_entries):
        stop = epg_entries[i+1]["start"]
    else:
        stop = "99999999999999 +0000"  # placeholder for last song

    xml.append(f'''  <programme start="{start}" stop="{stop}" channel="Radio">
    <title lang="en">{e["title"]}</title>
    <desc>{e["artist"]}</desc>
  </programme>''')

xml.append("</tv>")

with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print("epg.xml updated successfully.")
