import requests
from bs4 import BeautifulSoup
import datetime
import html
import vlc
import time
import threading

# === 1️⃣ Generate EPG XML ===
def generate_epg():
    url = "https://radio-online.my/988-fm-playlist"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    rows = soup.select("table tr")
    songs = []

    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) >= 3:
            time_str = cols[0].get_text(strip=True)
            artist = cols[1].get_text(strip=True)
            title = cols[2].get_text(strip=True)
            if artist and title and time_str:
                songs.append({"time": time_str, "artist": artist, "title": title})

    songs = songs[:33]

    tz = datetime.timezone(datetime.timedelta(hours=8))
    now = datetime.datetime.now(tz)
    start_times = []

    current_start = now
    for _ in songs:
        start_times.append(current_start)
        current_start += datetime.timedelta(minutes=3)

    stop_times = []
    for i in range(len(start_times)):
        if i + 1 < len(start_times):
            stop_times.append(start_times[i + 1] - datetime.timedelta(seconds=1))
        else:
            stop_times.append(start_times[i] + datetime.timedelta(minutes=3))

    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<tv date="{now.strftime("%Y%m%d%H%M%S")} +0800" '
        f'generator-info-url="https://sgolden58.github.io/radio/epg.xml" '
        f'source-info-url="https://sgolden58.github.io/radio/epg.xml?channel_id=988&amp;date={now.strftime("%Y%m%d")}">',
        '<channel id="988">',
        '<display-name>988</display-name>',
        '<icon src=""/>',
        '</channel>'
    ]

    for i, s in enumerate(songs):
        start_dt = start_times[i]
        stop_dt = stop_times[i]

        title_escaped = html.escape(s["title"], quote=True)
        desc_escaped = html.escape(s["artist"], quote=True)

        xml.append(f'<programme channel="988" start="{start_dt.strftime("%Y%m%d%H%M%S")} +0800" stop="{stop_dt.strftime("%Y%m%d%H%M%S")} +0800">')
        xml.append(f'  <title{s["title"]} + {s["artist"]}</title>')
        xml.append(f'  <desc>{s["artist"]}</desc>')
        xml.append(f'  <date>{s["time"]}</date>')
        xml.append('</programme>')

    xml.append('</tv>')

    with open("epg.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml))

    print(f"✅ EPG.xml generated — {len(songs)} songs.")

# === 2️⃣ VLC Radio Player ===
def create_vlc_player(url):
    try:
        vlc_instance = vlc.Instance()
        player = vlc_instance.media_player_new()
        media = vlc_instance.media_new(url)
        player.set_media(media)
        return player
    except Exception as e:
        print(f"Error creating VLC player: {e}")
        return None

def player_controls(player):
    print("\nControls:\n 'p' pause/play\n 's' stop\n 'q' quit")
    try:
        while True:
            action = input("\nEnter command: ").strip().lower()
            if action == 'p':
                if player.is_playing():
                    player.pause()
                    print("Paused.")
                else:
                    player.play()
                    print("Resumed.")
            elif action == 's':
                player.stop()
                print("Stopped.")
                break
            elif action == 'q':
                player.stop()
                print("Exiting.")
                break
            else:
                print("Invalid command.")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nExiting.")
        player.stop()

def main():
    # 1. Generate EPG XML
    generate_epg()

    # 2. Play live stream
    stream_url = "https://playerservices.streamtheworld.com/api/livestream-redirect/988_FM.mp3"
    print(f"Streaming live from: {stream_url}")

    player = create_vlc_player(stream_url)
    if player is None:
        return

    player.play()
    print("Playing live stream...")

    # 3. Start control loop
    player_controls(player)

if __name__ == "__main__":
    main()
