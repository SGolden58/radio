import requests
from bs4 import BeautifulSoup
import datetime

# === 1️⃣ Fetch playlist page ===
url = "https://radio-online.my/988-fm-playlist"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

# === 2️⃣ Extract songs from the playlist table ===
rows = soup.select("table tr")
songs = []

for row in rows[1:]:  # skip header
    cols = row.find_all("td")
    if len(cols) >= 3:
        time_str = cols[0].get_text(strip=True)
        artist = cols[1].get_text(strip=True)
        title = cols[2].get_text(strip=True)
        if artist and title and time_str:
            songs.append({"time": time_str, "artist": artist, "title": title})

# Limit to the latest 33 songs
songs = songs[:33]

# === 3️⃣ Prepare datetime objects ===
tz_myt = datetime.timezone(datetime.timedelta(hours=8))
now = datetime.datetime.now(tz_myt)  # this becomes your <tv date>
start_times = []

current_start = now  # first programme starts exactly at <tv date>

for s in songs:
    start_times.append(current_start)
    current_start += datetime.timedelta(minutes=3)  # each song = 3 min (adjust as needed)

# Prepare stop times (1 second before next song)
stop_times = []
for i in range(len(start_times)):
    if i + 1 < len(start_times):
        stop_times.append(start_times[i + 1] - datetime.timedelta(seconds=1))
    else:
        stop_times.append(start_times[i] + datetime.timedelta(minutes=3))  # last song

# === 4️⃣ Build XML EPG (Televizo)  ===
now = datetime.datetime.now(tz_myt)
xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<tv date="{now.strftime("%Y%m%d%H%M%S")} +0800" '
    f'generator-info-url="https://sgolden58.github.io/radio/epg.xml" '
    f'source-info-url="https://sgolden58.github.io/radio/epg.xml?channel_id=988&amp;date={now.strftime("%Y%m%d")}">',
    '<channel id="988">',
    '<display-name>988</display-name>',
    '<icon src=""/>',
    '</channel>'
]

# === 5️⃣ Add programme blocks ===
for i, s in enumerate(songs):
    start_dt = start_times[i]
    stop_dt = stop_times[i]

    # AM/PM format for <date>
    ampm_time = start_dt.strftime("%-I:%M %p")  # 5:38 PM (Linux/mac) use %-I, Windows might need %#I

    xml.append(f'<programme channel="988" start="{start_dt.strftime("%Y%m%d%H%M%S")} +0800" stop="{stop_dt.strftime("%Y%m%d%H%M%S")} +0800">')
    xml.append(f'  <title>{s["title"]} + {s["artist"]}</title>')
    xml.append(f'  <desc>{s["artist"]}</desc>')
    xml.append(f'  <date>{start_dt.strftime("%-I:%M %p")}</date>')
    xml.append('</programme>')

# === 6️⃣ Close XML ===
xml.append('</tv>')

# === 7️⃣ Save XML file ===
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print(f"✅ EPG.xml generated successfully — {len(songs)} songs with exact playlist times (Malaysia +0800).")

import requests

def get_radio_metadata(url):
    """
    Fetches the song and artist name from an internet radio stream.

    Args:
        url (str): https://playerservices.streamtheworld.com/api/livestream-redirect/988_FM.mp3

    Returns:
        tuple: A tuple containing the artist name and song title.
               Returns (None, None) if metadata cannot be retrieved.
    """
    try:
        # Request the stream with a header that asks for metadata
        headers = {'Icy-MetaData': '1'}
        response = requests.get(url, headers=headers, stream=True, timeout=10)
        
        # Check if the stream supports metadata
        if 'icy-metaint' not in response.headers:
            print("Error: Stream does not support Icy-MetaData protocol.")
            return None, None
        
        metaint = int(response.headers['icy-metaint'])
        
        # Read the first block of metadata
        response.raw.read(metaint)
        meta_byte = response.raw.read(1)
        if not meta_byte:
            return None, None
        
        meta_length = ord(meta_byte) * 16
        if meta_length == 0:
            return None, None

        metadata = response.raw.read(meta_length).decode('utf-8', errors='ignore')
        
        # Parse the StreamTitle from the metadata
        title_start = metadata.find("StreamTitle='")
        if title_start == -1:
            return None, None
            
        title_end = metadata.find("';", title_start)
        if title_end == -1:
            return None, None

        title_string = metadata[title_start + len("StreamTitle='"):title_end]
        
        # Split the string to get artist and song name
        if ' - ' in title_string:
            artist, song = title_string.split(' - ', 1)
            return artist.strip(), song.strip()
        
        return None, title_string.strip() # In case only the title is available
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None

if __name__ == "__main__":
    # Replace with the actual URL of your radio station stream
    stream_url = https://playerservices.streamtheworld.com/api/livestream-redirect/988_FM.mp3
    print(f"Attempting to connect to stream: {stream_url}")

    artist_name, song_title = get_radio_metadata(stream_url)
    
    if artist_name and song_title:
        print("\n--- Current Track Information ---")
        print(f"Artist: {artist_name}")
        print(f"Song:   {song_title}")
    elif song_title:
        print("\n--- Current Track Information ---")
        print(f"Song:   {song_title}")
    else:
        print("\nCould not retrieve track information.")

