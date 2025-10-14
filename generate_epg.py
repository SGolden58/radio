import requests
from bs4 import BeautifulSoup
import datetime
import html

# URL of your radio playlist
url = "https://radio-online.my/988-fm-playlist"

# Fetch the page
r = requests.get(url)
r.encoding = 'utf-8'  # ensure proper encoding
soup = BeautifulSoup(r.text, 'html.parser')

# Parse songs (adjust selector if necessary)
# Example: each song is in a <tr> with columns: time, title, artist
rows = soup.select("table tbody tr")  # adjust if needed
songs = []
for row in rows:
    cols = row.find_all("td")
    if len(cols) >= 2:
        time_text = cols[0].text.strip()  # e.g., '10:05'
        title = html.escape(cols[1].text.strip())
        artist = html.escape(cols[2].text.strip()) if len(cols) > 2 else "Unknown"
        songs.append({
            "time": time_text,
            "title": title,
            "artist": artist
        })

# Generate XML
now = datetime.datetime.now()
tz_offset = "+0800"

xml = [f'<tv date="{now.strftime("%Y%m%d%H%M%S")} {tz_offset}" '
       f'generator-info-url="https://yourwebsite.com/generator.html" '
       f'source-info-url="{url}?date={now.strftime("%Y%m%d")}&timezone=None">']

# Channel definition
xml.append('  <channel id="988">')
xml.append('    <display-name>988 FM</display-name>')
xml.append('  </channel>')

# Generate programmes
for i, song in enumerate(songs):
    hour, minute = map(int, song['time'].split(':'))
    start_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    # Estimate stop: next song's start or +10 mins if last
    if i + 1 < len(songs):
        next_hour, next_minute = map(int, songs[i+1]['time'].split(':'))
        stop_time = now.replace(hour=next_hour, minute=next_minute, second=0, microsecond=0)
    else:
        stop_time = start_time + datetime.timedelta(minutes=10)

    xml.append(f'  <programme channel="988" start="{start_time.strftime("%Y%m%d%H%M%S")} {tz_offset}" '
               f'stop="{stop_time.strftime("%Y%m%d%H%M%S")} {tz_offset}">')
    xml.append(f'    <title lang="zh">{song["title"]}</title>')
    xml.append(f'    <desc>{song["artist"]}</desc>')
    xml.append(f'    <date>{now.strftime("%Y-%m-%d")}</date>')
    xml.append('  </programme>')

xml.append('</tv>')

# Save XML
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print("EPG generated successfully.")
