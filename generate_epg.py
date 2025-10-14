import requests
from bs4 import BeautifulSoup
import datetime
import html

def generate_epg():
    # Fetch playlist data
    url = "https://radio-online.my/988-fm-playlist"
    r = requests.get(url)
    r.raise_for_status()
    
    soup = BeautifulSoup(r.text, "html.parser")
    songs_html = soup.select("table tr")
    songs = []

    # Parse song data
    for row in songs_html[1:]:  # Skip header
        cols = row.find_all("td")
        if len(cols) >= 2:
            time_str = cols[0].get_text(strip=True)
            title_artist = cols[1].get_text(strip=True)
            
            # Enhanced title-artist separation
            if " - " in title_artist:
                title, artist = title_artist.split(" - ", 1)
                artist = artist.strip()
                # Explicitly handle "Unknown" artist values
                if artist.lower() == "unknown":
                    artist = None
            else:
                title = title_artist
                artist = None
            
            songs.append({
                "time": time_str,
                "title": title,
                "artist": artist
            })

    # Build XML structure
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))  # MYT
    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<tv date="{now.strftime("%Y%m%d%H%M%S")} +0800" '
        f'generator-info-url="https://sgolden58.github.io/radio/epg.xml" '
        f'source-info-url="https://sgolden58.github.io/radio/epg.xml?channel_id=988">',
        '<channel id="988">',
        '<display-name lang="Malaysia">988</display-name>',
        '<icon src=""/>',
        '</channel>'
    ]

    # Generate programme entries
    for song in songs[:60]:  # Last 60 songs
        try:
            # Parse time with 24-hour format
            h, m = map(int, song["time"].split(":"))
            start = now.replace(hour=h, minute=m, second=0, microsecond=0)
            stop = start + datetime.timedelta(minutes=10)
        except ValueError:
            continue

        # XML-safe formatting
        title_escaped = html.escape(song['title'])
        artist_escaped = html.escape(song['artist']) if song['artist'] else None

        # Title construction logic
        if artist_escaped:
            formatted_title = f"{title_escaped} + {artist_escaped}"
        else:
            formatted_title = title_escaped

        # Description handling
        formatted_desc = artist_escaped if artist_escaped else "Unknown"

        xml.append(f'''<programme channel="988" start="{start.strftime("%Y%m%d%H%M%S")} +0000" stop="{stop.strftime("%Y%m%d%H%M%S")} +0000">
    <title lang="zh">{formatted_title}</title>
    <desc>{formatted_desc}</desc>
    <date>{song["time"]}</date>
</programme>''')

    xml.append("</tv>")

    # Write output
    with open("epg.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml))

if __name__ == "__main__":
    generate_epg()
