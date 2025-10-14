import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

URL = "https://radio-online.my/988-fm-playlist"
OUTPUT_FILE = "epg.xml"

def fetch_songs():
    r = requests.get(URL, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    rows = soup.select("table tbody tr")

    songs = []
    for row in rows[:10]:  # get up to 10 rows
        cols = [c.text.strip() for c in row.find_all("td")]
        if len(cols) >= 3:
            time_str, artist, title = cols[:3]
            songs.append((time_str, artist, title))
    return songs

def build_epg(songs):
    now = datetime.now()
    epg = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<tv generator-info-name="Radio-EPG">'
    ]
    epg.append('<channel id="988">')
    epg.append('  <display-name>988 FM</display-name>')
    epg.append('</channel>')

    if not songs:
        songs = [("00:00", "Unknown Artist", "No data")] * 10

    start_time = now.replace(minute=0, second=0, microsecond=0)

    for i in range(10):
        if i < len(songs):
            time_str, artist, title = songs[i]
        else:
            artist, title = "Unknown Artist", "No Data"
        start = start_time + timedelta(minutes=i * 5)   # each song = 5 mins
        stop = start + timedelta(minutes=5)
        start_fmt = start.strftime("%Y%m%d%H%M%S") + " +0800"
        stop_fmt = stop.strftime("%Y%m%d%H%M%S") + " +0800"

        epg.append(f'<programme start="{start_fmt}" stop="{stop_fmt}" channel="988">')
        epg.append(f'  <title lang="en">{title}</title>')
        epg.append(f'  <desc lang="en">{artist}</desc>')
        epg.append('</programme>')

    epg.append("</tv>")
    return "\n".join(epg)

def save_epg(xml):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(xml)

def main():
    songs = fetch_songs()
    xml = build_epg(songs)
    save_epg(xml)
    print("✅ epg.xml created with 10 songs")

if __name__ == "__main__":
    main()
