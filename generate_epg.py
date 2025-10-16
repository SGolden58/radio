

import requests

def get_radio_metadata(url):
    """
    Fetches the song and artist name from an internet radio stream.

    Args:
        url (str): https://playerservices.streamtheworld.com/api/livestream-redirect/988_FM.mp3

    Returns:
        tuple: A tuple containing the artist name and song title.
               Returns (None, None) if metadata cannot be retrieved.
    """
    try:
        # Request the stream with a header that asks for metadata
        headers = {'Icy-MetaData': '1'}
        response = requests.get(url, headers=headers, stream=True, timeout=10)
        
        # Check if the stream supports metadata
        if 'icy-metaint' not in response.headers:
            print("Error: Stream does not support Icy-MetaData protocol.")
            return None, None
        
        metaint = int(response.headers['icy-metaint'])
        
        # Read the first block of metadata
        response.raw.read(metaint)
        meta_byte = response.raw.read(1)
        if not meta_byte:
            return None, None
        
        meta_length = ord(meta_byte) * 16
        if meta_length == 0:
            return None, None

        metadata = response.raw.read(meta_length).decode('utf-8', errors='ignore')
        
        # Parse the StreamTitle from the metadata
        title_start = metadata.find("StreamTitle='")
        if title_start == -1:
            return None, None
            
        title_end = metadata.find("';", title_start)
        if title_end == -1:
            return None, None

        title_string = metadata[title_start + len("StreamTitle='"):title_end]
        
        # Split the string to get artist and song name
        if ' - ' in title_string:
            artist, song = title_string.split(' - ', 1)
            return artist.strip(), song.strip()
        
        return None, title_string.strip() # In case only the title is available
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None

if __name__ == "__main__":
    # Replace with the actual URL of your radio station stream
    stream_url = "https://playerservices.streamtheworld.com/api/livestream-redirect/988_FM.mp3"
    print(f"Attempting to connect to stream: {stream_url}")

    artist_name, song_title = get_radio_metadata(stream_url)
    
    if artist_name and song_title:
        print("\n--- Current Track Information ---")
        print(f"Artist: {artist_name}")
        print(f"Song:   {song_title}")
    elif song_title:
        print("\n--- Current Track Information ---")
        print(f"Song:   {song_title}")
    else:
        print("\nCould not retrieve track information.")

