import vlc
import time
import requests
from bs4 import BeautifulSoup
import datetime

# Function to get a radio station URL from the user (with default)
def get_stream_url():
    """Prompts the user for a radio station URL, defaults to 988 FM."""
    default_url = "https://playerservices.streamtheworld.com/api/livestream-redirect/988_FM.mp3"
    user_input = input(f"Enter stream URL or press Enter for default 988 FM ({default_url}): ").strip()
    return user_input if user_input else default_url

def create_vlc_player(url):
    """
    Creates and configures a VLC media player instance for the given stream.
    """
    try:
        # Create a VLC instance
        vlc_instance = vlc.Instance()
        
        # Create a new media player object
        player = vlc_instance.media_player_new()
        
        # Create a media object from the URL
        media = vlc_instance.media_new(url)
        
        # Set the media to the player
        player.set_media(media)
        
        return player
        
    except Exception as e:
        print(f"❌ Error creating VLC player (ensure VLC is installed): {e}")
        return None

def fetch_current_programme(epg_url="https://sgolden58.github.io/radio/epg.xml"):
    """
    Fetches and parses the current programme from the EPG XML.
    Returns a dict with 'title' and 'desc' if found, else None.
    """
    try:
        r = requests.get(epg_url, timeout=5)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "xml")
        
        # Get current time in UTC+8 for comparison
        tz = datetime.timezone(datetime.timedelta(hours=8))
        now = datetime.datetime.now(tz)
        now_str = now.strftime("%Y%m%d%H%M%S")
        
        # Find programmes where start <= now < stop
        programmes = soup.find_all("programme")
        for prog in programmes:
            start = prog.get("start").replace(" +0800", "")
            stop = prog.get("stop").replace(" +0800", "")
            if start <= now_str < stop:
                title = prog.find("title").get_text() if prog.find("title") else "Unknown"
                desc = prog.find("desc").get_text() if prog.find("desc") else "Unknown"
                return {"title": title, "desc": desc}
        
        return None  # No current programme
    except Exception as e:
        print(f"⚠️ Could not fetch EPG: {e}")
        return None

def main():
    """Main function to run the radio player application with EPG display."""
    stream_url = get_stream_url()
    
    if not stream_url:
        print("❌ No URL provided. Exiting.")
        return

    player = create_vlc_player(stream_url)
    if player is None:
        return
    
    print(f"🎵 Starting stream from: {stream_url}")
    player.play()
    
    # Wait a bit for stream to buffer
    time.sleep(2)
    
    # Fetch initial programme info
    current_prog = fetch_current_programme()
    if current_prog:
        print(f"📻 Now Playing: {current_prog['title']} by {current_prog['desc']}")
    else:
        print("📻 EPG not available or no current programme.")
    
    # Controls
    print("\n🎮 Controls:")
    print(" 'p' to pause/play")
    print(" 's' to stop")
    print(" 'i' to show current programme info")
    print(" 'v' to adjust volume (enter 0-100)")
    print(" 'q' to quit")
    
    last_epg_check = time.time()
    try:
        while True:
            action = input("\nEnter command: ").strip().lower()
            if action == 'p':
                if player.is_playing():
                    player.pause()
                    print("⏸️ Stream paused.")
                else:
                    player.play()
                    print("▶️ Stream resumed.")
            elif action == 's':
                player.stop()
                print("⏹️ Stream stopped.")
                break
            elif action == 'i':
                current_prog = fetch_current_programme()
                if current_prog:
                    print(f"📻 Current Programme: {current_prog['title']} by {current_prog['desc']}")
                else:
                    print("📻 No current programme info available.")
            elif action == 'v':
                try:
                    vol = int(input("Enter volume (0-100): ").strip())
                    player.audio_set_volume(max(0, min(100, vol)))
                    print(f"🔊 Volume set to {vol}%")
                except ValueError:
                    print("❌ Invalid volume. Enter a number 0-100.")
            elif action == 'q':
                player.stop()
                print("👋 Exiting.")
                break
            else:
                print("❌ Invalid command. Use 'p', 's', 'i', 'v', or 'q'.")
            
            # Auto-update EPG every 30 seconds while playing
            if time.time() - last_epg_check > 30 and player.is_playing():
                current_prog = fetch_current_programme()
                if current_prog:
                    print(f"🔄 Updated: Now Playing - {current_prog['title']} by {current_prog['desc']}")
                last_epg_check = time.time()
            
            time.sleep(0.5)  # Avoid high CPU usage
            
    except KeyboardInterrupt:
        print("\n👋 Keyboard interrupt. Exiting player.")
        player.stop()

if __name__ == "__main__":
    main()
