import os
import subprocess
import threading
import requests
import time
from bs4 import BeautifulSoup

# ---- CONFIGURATION ----
RADIO_URL = "https://playerservices.streamtheworld.com/api/livestream-redirect/988_FM.mp3"
ON_AIR_URL = "https://www.988.com.my/on-air/"
OUT_DIR = "hls988"
NOW_PLAYING_FILE = "nowplaying.txt"
LOGO = "logo.png"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # Change if needed
# ------------------------

def fetch_song():
    """Scrape 988 website for current song title."""
    try:
        r = requests.get(ON_AIR_URL, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        song = soup.select_one(".played-song__item")
        if song:
            return song.get_text(strip=True)
    except Exception as e:
        print("Fetch error:", e)
    return "988 FM Live Radio"

def update_nowplaying():
    """Continuously update nowplaying.txt every 30 seconds."""
    while True:
        title = fetch_song()
        with open(NOW_PLAYING_FILE, "w", encoding="utf-8") as f:
            f.write(title)
        print("Now playing:", title)
        time.sleep(30)

def start_ffmpeg():
    """Generate live visualizer video with HLS output."""
    os.makedirs(OUT_DIR, exist_ok=True)

    # FFmpeg visualizer effect (shows moving colored waves based on audio)
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-i", RADIO_URL,  # live audio input
        "-filter_complex",
        (
            "showcqt=fps=30:size=1280x720:count=1:bar_g=2:bar_v=2:basefreq=100:sono_g=3,"
            f"drawtext=fontfile={FONT}:textfile={NOW_PLAYING_FILE}:reload=1:x=50:y=h-80:"
            "fontcolor=white:fontsize=32:box=1:boxcolor=0x00000099,"
            f"movie={LOGO}[logo];[0:v][logo]overlay=main_w-overlay_w-40:40"
        ),
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-c:a", "aac", "-b:a", "128k",
        "-f", "hls",
        "-hls_time", "6",
        "-hls_list_size", "6",
        "-hls_flags", "delete_segments",
        os.path.join(OUT_DIR, "index.m3u8"),
    ]

    subprocess.run(ffmpeg_cmd)

if __name__ == "__main__":
    threading.Thread(target=update_nowplaying, daemon=True).start()
    time.sleep(3)
    start_ffmpeg()
