from datetime import datetime, timedelta

# OUTPUT XML FILE
output_file = "epg.xml"

# CHANNEL INFO
channel_id = "988"
channel_name = "988 FM"
channel_logo = "https://raw.githubusercontent.com/SGolden58/svg/main/Logo/988.png"

# SONG LIST (replace with your songs/artists)
songs = [
    ("Song 1", "Artist 1"),
    ("Song 2", "Artist 2"),
    ("Song 3", "Artist 3"),
    ("Song 4", "Artist 4"),
    ("Song 5", "Artist 5"),
    ("Song 6", "Artist 6"),
    ("Song 7", "Artist 7"),
    ("Song 8", "Artist 8"),
    ("Song 9", "Artist 9"),
    ("Song 10", "Artist 10"),
]

# START TIME
start_time = datetime.now().replace(minute=0, second=0, microsecond=0)

# WRITE XML
with open(output_file, "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write(f'<tv generator-info-name="Radio EPG Script">\n')
    f.write(f'  <channel id="{channel_id}">\n')
    f.write(f'    <display-name>{channel_name}</display-name>\n')
    f.write(f'    <icon src="{channel_logo}"/>\n')
    f.write(f'  </channel>\n\n')

    for i, (title, artist) in enumerate(songs):
        start = start_time + timedelta(minutes=5*i)
        stop = start + timedelta(minutes=5)
        start_str = start.strftime("%Y%m%d%H%M%S +0800")
        stop_str = stop.strftime("%Y%m%d%H%M%S +0800")
        date_str = start.strftime("%Y-%m-%d")

        f.write(f'  <programme channel="{channel_id}" start="{start_str}" stop="{stop_str}">\n')
        f.write(f'    <title lang="zh">{title}</title>\n')
        f.write(f'    <desc>{artist}</desc>\n')
        f.write(f'    <date>{date_str}</date>\n')
        f.write(f'  </programme>\n\n')

    f.write('</tv>')
