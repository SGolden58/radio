import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Fetch radio playlist page
url = "https://radio-online.my/988-fm-playlist"
res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

rows = soup.select("table tbody tr")

songs = []
for row in rows:
    cols = [c.text.strip() for c in row.find_all("td")]
    if len(cols) >= 3:
        time_str, artist, title = cols
        try:
            # Parse HH:MM as today's time
            now = datetime.now()
            start = datetime.strptime(time_str, "%H:%M").replace(
                year=now.year, month=now.month, day=now.day)
            stop = start + timedelta(minutes=5)
            songs.append((start, stop, artist, title))
        except Exception as e:
            print("Skipping:", e)

xml = '<?xml version="1.0" encoding="UTF-8"?>\n<tv generator-info-name="Radio EPG Script">\n'
xml += '  <channel id="988fm.my"><display-name>988 FM</display-name></channel>\n'

for s in songs:
    start, stop, artist, title = s
    xml += f'  <programme start="{start.strftime("%Y%m%d%H%M%S")} +0800" stop="{stop.strftime("%Y%m%d%H%M%S")} +0800" channel="988fm.my">\n'
    xml += f'    <title lang="en">{title}</title>\n'
    xml += f'    <desc>{artist}</desc>\n'
    xml += '  </programme>\n'

xml += '</tv>\n'

with open("epg.xml", "w", encoding="utf-8") as f:
    f.write(xml)
