import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# --- Step 1: Fetch playlist page ---
url = "https://radio-online.my/988-fm-playlist"
res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

# --- Step 2: Extract table rows ---
rows = soup.select("table tbody tr")

songs = []
for row in rows:
    cols = [c.text.strip() for c in row.find_all("td")]
    if len(cols) >= 3:
        # Only take the first 3 columns
        time_str, artist, title = cols[:3]
        try:
            now = datetime.now()
            start = datetime.strptime(time_str, "%H:%M").replace(
                year=now.year, month=now.month, day=now.day)
            stop = start + timedelta(minutes=5)
            songs.append((start, stop, artist, title))
        except Exception as e:
            print("Skipping row:", e)

# --- Step 3: Generate XML ---
xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
xml += '<tv generator-info-name="Radio EPG Script">\n'
xml += '  <channel id="988"><display-name>988</display-name></channel>\n'

for s in songs:
    start, stop, artist, title = s
    xml += f'  <programme start="{start.strftime("%Y%m%d%H%M%S")} +0800" stop="{stop.strftime("%Y%m%d%H%M%S")} +0800" channel="988">\n'
    xml += f'    <title lang="en">{title}</title>\n'
    xml += f'    <desc>{artist}</desc>\n'
    xml += '  </programme>\n'

xml += '</tv>\n'

# --- Step 4: Save to epg.xml ---
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write(xml)

print(f"EPG XML generated with {len(songs)} entries.")
