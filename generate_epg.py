import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import html

# Your radio playlist URL
url = "https://radio-online.my/988-fm-playlist"

# Fetch the page
r = requests.get(url)
r.raise_for_status()  # stop if request failed

soup = BeautifulSoup(r.text, "html.parser")

# Find song entries (adjust selectors based on page structure)
songs = []
rows = soup.select("table tr")  # assuming songs are in table rows
for tr in rows:
    tds = tr.find_all("td")
    if len(tds) >= 2:
        time_str = tds[0].get_text(strip=True)
        title = tds[1].get_text(strip=True)
        songs.append((time_str, title))

# Build XML
now = datetime.utcnow()
xml = [f'<?xml version="1.0" encoding="UTF-8"?>']
xml.append(f'<tv date="{now.strftime("%Y%m%d%H%M%S")} +0800" generator-info-url="https://radio-online.my/988-fm-playlist" source-info-url="{url}">')
xml.append('<channel id="988"></channel>')

for i, (time_str, title) in enumerate(songs):
    try:
        start = datetime.strptime(time_str, "%H:%M")
        start = datetime.utcnow().replace(hour=start.hour, minute=start.minute, second=0, microsecond=0)
        stop = start + timedelta(minutes=10)
    except:
        start = now - timedelta(minutes=i*10)
        stop = start + timedelta(minutes=10)
    
    xml.append(f'''<programme channel="988" start="{start.strftime("%Y%m%d%H%M%S")} +0000" stop="{stop.strftime("%Y%m%d%H%M%S")} +0000">
<title lang="zh">{html.escape(title)}</title>
<desc>Unknown</desc>
<date>{start.strftime("%Y-%m-%d")}</date>
</programme>''')

xml.append('</tv>')

with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))
