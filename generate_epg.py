import requests
from bs4 import BeautifulSoup
import datetime
import html
import yaml
import os

# Load YAML configuration
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

refresh_duration = config.get("refresh_duration_minutes", 10)

# Check if the EPG file exists and read the last refresh time
epg_file = "epg.xml"
last_refresh_time = None

if os.path.exists(epg_file):
    # Get the last modification time of the file
    last_refresh_time = datetime.datetime.fromtimestamp(os.path.getmtime(epg_file))

# Determine if we need to refresh based on the last refresh time
now = datetime.datetime.utcnow()
if last_refresh_time and (now - last_refresh_time).total_seconds() < refresh_duration * 60:
    print("Using existing EPG data, no refresh needed.")
    with open(epg_file, "r", encoding="utf-8") as f:
        epg_data = f.read()
    print(epg_data)
    exit()

# URL of the radio station's playlist
url = "https://radio-online.my/988-fm-playlist"

# Fetch the HTML content
try:
    r = requests.get(url)
    r.raise_for_status()
except requests.RequestException as e:
    print(f"Error fetching the URL: {e}")
    exit(1)

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(r.text, "html.parser")

# Select the relevant table rows containing song data
songs_html = soup.select("table tr")  # Adjust this selector if needed
songs = []

# Extract song details from the HTML
for row in songs_html[1:]:  # Skip header row
    cols = row.find_all("td")
    if len(cols) >= 3:
        time_str = cols[0].get_text(strip=True)
        artist_title = cols[1].get_text(strip=True)
        additional_info = cols[2].get_text(strip=True) if len(cols) > 2 else ""
        
        # Split artist and title based on the format
        if " - " in artist_title:
            artist, title = artist_title.split(" - ", 1)
        else:
            title, artist = artist_title, "Unknown"

        songs.append({
            "time": time_str,
            "title": title,
            "artist": artist,
            "additional_info": additional_info
        })

# Build XML structure for EPG
xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<tv date="{} +0800" generator-info-url="https://sgolden58.github.io/radio/epg.xml" source-info-url="https://sgolden58.github.io/radio/epg.xml?channel_id=988&amp;date={}">'.format(
        now.strftime("%Y%m%d%H%M%S"), now.strftime("%Y-%m-%d")),
    '<channel id="988">',
    '<display-name lang="Malaysia">988</display-name>',
    '<icon src=""/>'
]

# Generate program entries in the XML
for s in songs:
    # Parse time string, assuming format HH:MM
    try:
        h, m = map(int, s["time"].split(":"))
        start = now.replace(hour=h, minute=m, second=0, microsecond=0)
        stop = start + datetime.timedelta(minutes=1)  # Each song lasts 1 minute
    except ValueError:
        print(f"Invalid time format: {s['time']}. Using current time instead.")
        start = now
        stop = start + datetime.timedelta(minutes=1)

    # Escape special characters in title and artist
    title = html.escape(s['title']).replace('&', '&amp;')
    artist = html.escape(s['artist']).replace('&', '&amp;')

    # Combine title and artist for the <title> tag
    combined_title = f"{title} + {artist}"

    # Append programme entry with combined title in the correct tags
    xml.append(f'''  <programme channel="988" start="{start.strftime("%Y%m%d%H%M%S")} +0000" stop="{stop.strftime("%Y%m%d%H%M%S")} +0000">
    <title lang="zh">{combined_title}</title>
    <desc>{artist}</desc>
  </programme>''')

# Close the XML structure properly
xml.append('</channel>')  # Close channel tag
xml.append('</tv>')       # Close tv tag

# Write the XML to a file
try:
    with open(epg_file, "w", encoding="utf-8") as f:
        f.write("\n".join(xml))
    print("EPG XML generated successfully.")
except IOError as e:
    print(f"Error writing to file: {e}")
