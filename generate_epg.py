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

for row in rows[1:]:  # Skip header
    cols = row.find_all("td")
    if len(cols) >= 3:
        time_str = cols[0].get_text(strip=True)
        artist = cols[1].get_text(strip=True)
        title = cols[2].get_text(strip=True)
        if artist and title and time_str:
            songs.append({"time": time_str, "artist": artist, "title": title})

# Limit to latest 33 songs
songs = songs[:33]

# === 3️⃣ Improved time parsing (AM/PM first, then 24-hour fallback) ===
tz = datetime.timezone(datetime.timedelta(hours=8))
now = datetime.datetime.now(tz)
today = now.date()
start_times = []

for s in songs:
    time_str = s["time"].strip().upper()
    try:
        # First try AM/PM format (e.g., "2:30 PM")
        dt_obj = datetime.datetime.strptime(time_str, "%I:%M %p")
        h = dt_obj.hour
        m = dt_obj.minute
    except ValueError:
        try:
            # Fallback to 24-hour format (e.g., "14:30")
            h, m = map(int, time_str.split(":"))
        except ValueError:
            print(f"⚠️ Skipped invalid time: {time_str}")
            continue
    
    # Create datetime for today
    dt = datetime.datetime(today.year, today.month, today.day, h, m, 0, tzinfo=tz)
    
    # Skip if time is in the past (to avoid old programmes)
    if dt < now:
        continue
    
    start_times.append(dt)

# Re-limit songs to match valid start_times
songs = songs[:len(start_times)]

# === 4️⃣ Prepare stop times ===
stop_times = []
for i in range(len(start_times)):
    if i + 1 < len(start_times):
        stop_times.append(start_times[i + 1] - datetime.timedelta(seconds=1))
    else:
        stop_times.append(start_times[i] + datetime.timedelta(minutes=2))  # Last song: arbitrary 2 min

# === 5️⃣ XML header ===
xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<tv date="{now.strftime("%Y%m%d%H%M%S")} +0800" '
    f'generator-info-url="https://sgolden58.github.io/radio/epg.xml" '
    f'source-info-url="https://sgolden58.github.io/radio/epg.xml?channel_id=988&amp;date={now.strftime("%Y%m%d")}&amp;timezone=None">',
    '<channel id="988">',
    '<display-name lang="zh">988</display-name>',  # Reverted to Chinese for the channel
    '<icon src=""/>',
    '</channel>'
]

# === 6️⃣ Add programmes (swapped title/desc for better display) ===
for i, s in enumerate(songs):
    start_dt = start_times[i]
    stop_dt = stop_times[i]

    # Swap: title = song title, desc = artist
    title_escaped = html.escape(s["title"], quote=True)  # Song title as main title
    desc_escaped = html.escape(s["artist"], quote=True)  # Artist as description

    xml.append(f'<programme channel="988" start="{start_dt.strftime("%Y%m%d%H%M%S")} +0800" stop="{stop_dt.strftime("%Y%m%d%H%M%S")} +0800">')
    xml.append(f'  <title lang="zh">{title_escaped}</title>')  # Reverted to Chinese
    xml.append(f'  <desc lang="zh">{desc_escaped}</desc>')  # Reverted to Chinese
    xml.append(f'  <date>{s["time"]}</date>')
    xml.append('</programme>')

# === 7️⃣ Close XML ===
xml.append('</tv>')

# === 8️⃣ Save XML ===
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

print(f"✅ EPG.xml generated — {len(songs)} future songs, times parsed with AM/PM priority")
