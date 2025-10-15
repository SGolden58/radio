import requests
from bs4 import BeautifulSoup
import datetime
import html

# === 1️⃣ Fetch playlist page ===
url = "https://radio-online.my/988-fm-playlist"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

# === 2️⃣ Extract songs from table ===
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

# === 3️⃣ Prepare start times and stop times ===
tz = datetime.timezone(datetime.timedelta(hours=8))
today = datetime.datetime.now(tz).date()
start_times = []

# Time parsing with enhanced fallback
for s in songs:
    time_str = s["time"].strip().lower()
    try:
        time_obj = datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        try:
            time_obj = datetime.strptime(time_str, "%I:%M %p").time()
        except:
            # Enhanced raw split with AM/PM detection
            if 'am' in time_str or 'pm' in time_str:
                h_part = time_str.split('am')[0].split('pm')[0]
                h, m = map(int, h_part.split(':'))
                h += 12 if 'pm' in time_str and h < 12 else 0
            else:
                h, m = map(int, time_str.split(':'))
            time_obj = time(h, m)
    
    dt = datetime.combine(today, time_obj).replace(tzinfo=tz)
    start_times.append(dt)

# Stop time calculation
stop_times = []
for i in range(len(start_times)):
    if i + 1 < len(start_times):
        stop_time = start_times[i+1] - timedelta(seconds=1)
    else:
        # Use average song duration (3.5 minutes)
        stop_time = start_times[i] + timedelta(minutes=3, seconds=30)
    
    # Midnight correction
    if stop_time.day != start_times[i].day:
        stop_time = stop_time.replace(
            hour=23, minute=59, second=59, microsecond=0
        )
    
    stop_times.append(stop_time)

# === 4️⃣ XML header ===
now = datetime.datetime.now(tz)
xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<tv date="{now.strftime("%Y%m%d%H%M%S")} +0800" '
    f'generator-info-url="https://sgolden58.github.io/radio/epg.xml" '
    f'source-info-url="https://sgolden58.github.io/radio/epg.xml?channel_id=988&amp;date={now.strftime("%Y%m%d")}&amp;timezone=None">',
    '<channel id="988">',
    '<display-name lang="zh">988</display-name>',
    '<icon src=""/>',
    '</channel>'
]

# === 5️⃣ Add programmes ===
for i, s in enumerate(songs):
    start_dt = start_times[i]
    stop_dt = stop_times[i]

    # Fixed: Preserve original time format
    try:
        original_time = datetime.datetime.strptime(s["time"], "%I:%M %p").strftime("%I:%M %p")
    except ValueError:
        original_time = s["time"]  # Fallback to raw string

    title_escaped = html.escape(s["artist"], quote=True)
    desc_escaped = html.escape(s["title"], quote=True)

    xml.append(f'<programme channel="988" start="{start_dt.strftime("%Y%m%d%H%M%S")} +0800" stop="{stop_dt.strftime("%Y%m%d%H%M%S")} +0800">')
    xml.append(f'  <title lang="zh">{title_escaped}</title>')
    xml.append(f'  <desc lang="zh">{desc_escaped}</desc>')
    xml.append(f'  <date>{original_time}</date>')
    xml.append('</programme>')

# === 6️⃣ Close XML ===
xml.append('</tv>')

# === 7️⃣ Save XML ===
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print(f"✅ EPG.xml generated — {len(songs)} songs, time conversion fixed")
