import requests
from bs4 import BeautifulSoup
import datetime
import html

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
    if len(cols) >= 2:
        time_str = cols[0].get_text(strip=True)
        title_artist = cols[1].get_text(strip=True)
        if " - " in title_artist:
            title, artist = title_artist.split(" - ", 1)
        else:
            title, artist = title_artist, "Unknown"
        songs.append({
            "time": time_str,
            "title": title,
            "artist": artist
        })

# Build XML structure for EPG
now = datetime.datetime.utcnow()
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
        stop = start + datetime.timedelta(minutes=10)  # Each song lasts 10 minutes
    except ValueError:
        print(f"Invalid time format: {s['time']}. Using current time instead.")
        start = now
        stop = start + datetime.timedelta(minutes=10)

    # Escape special characters in title and artist
    title = html.escape(s['title']).replace('&', '&amp;')
    artist = html.escape(s['artist']).replace('&', '&amp;')

    # Append programme entry
    xml.append(f'''  <programme channel="988" start="{start.strftime("%Y%m%d%H%M%S")} +0000" stop="{stop.strftime("%Y%m%d%H%M%S")} +0000">
    <title lang="zh">{title}</title>
    <desc>{artist}</desc>
  </programme>''')

# Close the XML structure properly
xml.append('</channel>')  # Close channel tag
xml.append('</tv>')       # Close tv tag

# Debugging: Check the final XML structure
print("\n".join(xml))

# Write the XML to a file
try:
    with open("epg.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml))
    print("EPG XML generated successfully.")
except IOError as e:
    print(f"Error writing to file: {e}")
