import datetime
import html
import json

# Load songs from JSON (replace this with your API call if needed)
with open("songs.json", "r", encoding="utf-8") as f:
    songs = json.load(f)

now = datetime.datetime.now()
output = []

output.append('<?xml version="1.0" encoding="UTF-8"?>')
output.append(
    f'<tv date="{now.strftime("%Y%m%d%H%M%S")} +0800" '
    'generator-info-url="https://sgolden58.github.io/radio/epg.xml" '
    f'source-info-url="https://sgolden58.github.io/radio/epg.xml?channel_id=988&amp;date={now.strftime("%Y%m%d")}&amp;timezone=None">'
)
output.append('<channel id="988">')
output.append('<display-name>SGolden Radio</display-name>')
output.append('</channel>')

for song in reversed(songs):
    start_time = datetime.datetime.strptime(song["time"], "%Y-%m-%d %H:%M:%S")
    stop_time = start_time + datetime.timedelta(minutes=3)

    start_str = start_time.strftime("%Y%m%d%H%M%S") + " +0800"
    stop_str = stop_time.strftime("%Y%m%d%H%M%S") + " +0800"

    title = html.escape(song["title"])
    artist = html.escape(song["artist"])
    desc = f"{artist} - {title}"

    output.append(f'<programme start="{start_str}" stop="{stop_str}" channel="988">')
    output.append(f'  <title lang="en">{artist} - {title}</title>')
    output.append(f'  <desc lang="en">{desc}</desc>')
    output.append('</programme>')

output.append('</tv>')

with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("✅ EPG.xml generated successfully.")
