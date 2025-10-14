import html  # ADD THIS

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

        # Escape special XML characters here ⬇️
        artist = html.escape(artist)
        title = html.escape(title)

        start = start_time + timedelta(minutes=i * 5)
        stop = start + timedelta(minutes=5)
        start_fmt = start.strftime("%Y%m%d%H%M%S") + " +0800"
        stop_fmt = stop.strftime("%Y%m%d%H%M%S") + " +0800"

        epg.append(f'<programme start="{start_fmt}" stop="{stop_fmt}" channel="988">')
        epg.append(f'  <title lang="en">{title}</title>')
        epg.append(f'  <desc lang="en">{artist}</desc>')
        epg.append('</programme>')

    epg.append("</tv>")
    return "\n".join(epg)
