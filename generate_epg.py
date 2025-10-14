import datetime
import html

# Assume you already have your real 'songs' list from your source
# Each item must contain:
#   song["time"]  → "YYYY-MM-DD HH:MM:SS"
#   song["artist"]
#   song["title"]

# Example:
# songs = get_song_list_from_api()

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

# ⚡ Newest songs appear first
for song in reversed(songs):
    start_time = datetime.datetime.strptime(song["time"], "%Y-%m-%d %H:%M:%S")
    stop_time = start_time + datetime.timedelta(minutes=3)  # each song = 3 minutes

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

# Save file
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("✅ EPG.xml generated successfully.")
