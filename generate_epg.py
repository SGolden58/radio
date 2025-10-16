import requests
import html
from datetime import datetime

def fetch_playlist(station_id=12):
    url = "https://online-radio.my/api-backend.php"
    payload = {"id": station_id, "action": "station-playlist-history"}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

def generate_xml_from_playlist(playlist):
    now = datetime.now()
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<playlist date="{now.strftime("%Y-%m-%d")}">',
    ]

    for item in playlist:
        artist = item.get("artist", "").strip()
        title = item.get("title", "").strip()
        time_str = item.get("time", "").strip()  # e.g. "22:00"

        # Format times for XML attributes (assuming today)
        try:
            dt = datetime.strptime(time_str, "%H:%M")
            start_str = dt.strftime("%Y%m%d%H%M%S")
            # For demo, stop time = start + 3 minutes
            stop_dt = dt.replace(minute=dt.minute + 3)
            stop_str = stop_dt.strftime("%Y%m%d%H%M%S")
        except Exception:
            start_str = stop_str = ""

        artist_esc = html.escape(artist)
        title_esc = html.escape(title)

        xml_lines.append(f'  <programme start="{start_str}" stop="{stop_str}">')
        xml_lines.append(f'    <title>{title_esc}</title>')
        xml_lines.append(f'    <artist>{artist_esc}</artist>')
        xml_lines.append(f'  </programme>')

    xml_lines.append('</playlist>')
    return "\n".join(xml_lines)

if __name__ == "__main__":
    data = fetch_playlist()
    playlist = data.get("playlist", [])  # Adjust key based on actual API response structure
    xml_output = generate_xml_from_playlist(playlist)
    print(xml_output)
