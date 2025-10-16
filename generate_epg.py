import requests
from bs4 import BeautifulSoup
import datetime
import html
import sys

def get_radio_metadata(url):
    """
    Fetches the song and artist name from an internet radio stream.
    """
    try:
        headers = {'Icy-MetaData': '1'}
        response = requests.get(url, headers=headers, stream=True, timeout=10)
        
        if 'icy-metaint' not in response.headers:
            print("Error: Stream does not support Icy-MetaData protocol.")
            return None, None
        
        metaint = int(response.headers['icy-metaint'])
        
        response.raw.read(metaint)
        meta_byte = response.raw.read(1)
        if not meta_byte:
            return None, None
        
        meta_length = ord(meta_byte) * 16
        if meta_length == 0:
            return None, None

        metadata = response.raw.read(meta_length).decode('utf-8', errors='ignore')
        
        title_start = metadata.find("StreamTitle='")
        if title_start == -1:
            return None, None
            
        title_end = metadata.find("';", title_start)
        if title_end == -1:
            return None, None

        title_string = metadata[title_start + len("StreamTitle='"):title_end]
        
        if ' - ' in title_string:
            artist, song = title_string.split(' - ', 1)
            return artist.strip(), song.strip()
        
        return None, title_string.strip()
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None

def generate_epg_from_playlist():
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
    now = datetime.datetime.now(tz_myt)  # current time in Malaysia timezone
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

    return songs, start_times, stop_times, tz_myt, now

def build_epg_xml(songs, start_times, stop_times, tz_myt, now, live_artist=None, live_song=None):
    if sys.platform.startswith('win'):
        hour_format = "%#I:%M %p"
    else:
        hour_format = "%-I:%M %p"

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

    # Add live metadata as first programme if available
    if live_artist or live_song:
        start_dt = now
        stop_dt = now + datetime.timedelta(minutes=3)
        title_escaped = html.escape(live_song if live_song else "")
        artist_escaped = html.escape(live_artist if live_artist else "")
        xml.append(f'<programme channel="988" start="{start_dt.strftime("%Y%m%d%H%M%S")} +0800" stop="{stop_dt.strftime("%Y%m%d%H%M%S")} +0800">')
        xml.append(f'  <title>{s["title"]} + {s["artist"]}</title>')
        xml.append(f'  <desc>{s["artist"]}</desc>')
        xml.append(f'  <date>{start_dt.strftime(hour_format)}</date>')
        xml.append('</programme>')

    # Add playlist programmes
    for i, s in enumerate(songs):
        start_dt = start_times[i]
        stop_dt = stop_times[i]

        title_escaped = html.escape(s["title"])
        artist_escaped = html.escape(s["artist"])

        xml.append(f'<programme channel="988" start="{start_dt.strftime("%Y%m%d%H%M%S")} +0800" stop="{stop_dt.strftime("%Y%m%d%H%M%S")} +0800">')
        xml.append(f'  <title>{s["title"]} + {s["artist"]}</title>')
        xml.append(f'  <desc>{s["artist"]}</desc>')
        xml.append(f'  <date>{start_dt.strftime(hour_format)}</date>')
        xml.append('</programme>')

    xml.append('</tv>')
    return "\n".join(xml)

if __name__ == "__main__":
    # Get live metadata from stream
    stream_url = "https://playerservices.streamtheworld.com/api/livestream-redirect/988_FM.mp3"
    print(f"Attempting to connect to stream: {stream_url}")
    live_artist, live_song = get_radio_metadata(stream_url)
    if live_artist and live_song:
        print(f"Live track: {live_artist} - {live_song}")
    elif live_song:
        print(f"Live track: {live_song}")
    else:
        print("Could not retrieve live track info.")

    # Generate playlist EPG data
    songs, start_times, stop_times, tz_myt, now = generate_epg_from_playlist()

    # Build combined XML with live metadata included
    epg_xml = build_epg_xml(songs, start_times, stop_times, tz_myt, now, live_artist, live_song)

    # Save to file
    with open("epg.xml", "w", encoding="utf-8") as f:
        f.write(epg_xml)

    print(f"✅ EPG.xml generated successfully with {len(songs)} playlist songs plus live metadata.")
