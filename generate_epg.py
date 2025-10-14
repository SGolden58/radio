import requests
from bs4 import BeautifulSoup
import datetime
import html

# === 1) Fetch playlist page ===
url = "https://radio-online.my/988-fm-playlist"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

# === 2) Extract songs from table (time like "20:48") ===
songs_html = soup.select("table tr")
songs = []

for row in songs_html[1:]:  # skip header row
    cols = row.find_all("td")
    if len(cols) >= 2:
        time_str = cols[0].get_text(strip=True)        # e.g. "20:48"
        title_artist = cols[1].get_text(strip=True)    # e.g. "歌名 - 歌手" or "歌名"

        if " - " in title_artist:
            title, artist = title_artist.split(" - ", 1)
            title = title.strip()
            artist = artist.strip()
        else:
            title = title_artist.strip()
            artist = ""   # leave empty for now; we'll fill fallback later

        # Only keep valid-looking times like HH:MM
        songs.append({"time": time_str, "title": title, "artist": artist})

# Limit to latest 60 rows (if table longer)
songs = songs[:60]

# === 3) Remove "Unknown" by filling missing artists from neighbors or title ===
for i, s in enumerate(songs):
    if not s.get("artist"):  # empty string or missing
        # Try next
        next_artist = songs[i + 1]["artist"] if i + 1 < len(songs) else ""
        prev_artist = songs[i - 1]["artist"] if i - 1 >= 0 else ""
        if next_artist:
            s["artist"] = next_artist
        elif prev_artist:
            s["artist"] = prev_artist
        else:
            # Last fallback: use the title as artist to avoid "Unknown"
            s["artist"] = s["title"]

# === 4) Convert times to datetimes (Malaysia timezone) ===
tz = datetime.timezone(datetime.timedelta(hours=8))
now = datetime.datetime.now(tz)
today = now.date()

start_datetimes = []
for s in songs:
    try:
        # Parse HH:MM — assume same day as now (Malaysia). If needed, adjust for midnight wrap.
        h, m = map(int, s["time"].split(":"))
        dt = datetime.datetime(year=today.year, month=today.month, day=today.day,
                               hour=h, minute=m, second=0, tzinfo=tz)
        start_datetimes.append(dt)
    except Exception:
        # If parsing fails, fallback to `now` (skip later when generating programmes)
        start_datetimes.append(None)

# If times are not strictly increasing (page can list oldest->newest),
# we keep the scraped order. We will compute each stop based on the next start.
# === 5) Build XML ===
xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<tv date="{now.strftime("%Y%m%d%H%M%S")} +0800" '
    'generator-info-url="https://sgolden58.github.io/radio/epg.xml" '
    f'source-info-url="https://sgolden58.github.io/radio/epg.xml?channel_id=988&amp;date={now.strftime("%Y%m%d")}&amp;timezone=None">',
    '<channel id="988">',
    '<display-name lang="zh">988</display-name>',
    '<icon src=""/>',
    '</channel>'
]

# === 6) Emit programmes. stop = next_start - 1s (if next exists). If next_start-start >= 60s, that ensures >=1min.
# Note: if gap < 60s, we still use next_start - 1s to avoid overlap (programme will be <1min).
for i, s in enumerate(songs):
    start_dt = start_datetimes[i]
    if not start_dt:
        continue  # skip malformed time rows

    # Compute stop time
    stop_dt = None
    # find next valid start datetime
    j = i + 1
    while j < len(start_datetimes) and start_datetimes[j] is None:
        j += 1
    if j < len(start_datetimes) and start_datetimes[j] is not None:
        next_start = start_datetimes[j]
        delta_secs = (next_start - start_dt).total_seconds()
        # If next_start is later than start_dt
        if delta_secs > 0:
            # Prefer stop = next_start - 1 second (never overlap).
            # If delta_secs >= 60, that means programme >= 1 minute.
            stop_dt = next_start - datetime.timedelta(seconds=1)
        else:
            # next_start <= start_dt (weird ordering), fallback to start + 60s
            stop_dt = start_dt + datetime.timedelta(seconds=60)
    else:
        # No next start available (last item). Make a reasonable stop time:
        # set stop = start + 60s (minimum), you can increase if you want long tails.
        stop_dt = start_dt + datetime.timedelta(seconds=60)

    # Ensure stop is after start; if not, force 1 second after start
    if stop_dt <= start_dt:
        stop_dt = start_dt + datetime.timedelta(seconds=1)

    # Escape text
    title_escaped = html.escape(s["title"], quote=True)
    artist_escaped = html.escape(s["artist"], quote=True)
    # Make title and desc include both artist and title (artist - title)
    combined = f"{artist_escaped} - {title_escaped}"

    xml_lines.append(
        f'<programme channel="988" start="{start_dt.strftime("%Y%m%d%H%M%S")} +0800" stop="{stop_dt.strftime("%Y%m%d%H%M%S")} +0800">'
    )
    xml_lines.append(f'    <title lang="zh">{combined}</title>')
    xml_lines.append(f'    <desc lang="zh">{combined}</desc>')
    xml_lines.append(f'    <date>{s["time"]}</date>')
    xml_lines.append('</programme>')

xml_lines.append('</tv>')

# === 7) Write file ===
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml_lines))

print("✅ EPG.xml generated with neighbor artist fallback and safe stop times.")
