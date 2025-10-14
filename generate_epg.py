import requests
from bs4 import BeautifulSoup
import yaml
from datetime import datetime, timedelta

def load_config():
    with open('update_epg.yml', 'r') as file:
        return yaml.safe_load(file)

def fetch_playlist(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {url}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    songs = []

    # Adjust these selectors based on the actual HTML structure
    for item in soup.select('.playlist-item'):  # Update this selector as needed
        title = item.select_one('.song-title').get_text(strip=True)  # Update this selector
        artist = item.select_one('.artist-name').get_text(strip=True)  # Update this selector
        songs.append({'title': title, 'artist': artist})

    return songs[:config['epg']['max_songs']]  # Limit to the configured max songs

def generate_xml(songs, config):
    now = datetime.now()
    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<tv date="{} {}" generator-info-url="{}" source-info-url="{}">'.format(
            now.strftime("%Y%m%d%H%M%S"), config['epg']['timezone'],
            config['epg']['generator_info_url'], config['epg']['generator_info_url']
        ),
        '<channel id="988">',
        '<display-name lang="Malaysia">988</display-name>',
        '<icon src=""/>'
    ]

    for song in songs:
        start_time = now.strftime("%Y%m%d%H%M%S")
        stop_time = (now + timedelta(minutes=config['epg']['programme_duration_minutes'])).strftime("%Y%m%d%H%M%S")
        xml.append('<programme start="{}" stop="{}">'.format(start_time, stop_time))
        xml.append('<title>{}</title>'.format(song['title']))
        xml.append('<desc>{}</desc>'.format(song['artist']))
        xml.append('</programme>')
        now += timedelta(minutes=config['epg']['programme_duration_minutes'])  # Increment time

    xml.append('</channel>')
    xml.append('</tv>')
    
    return "\n".join(xml)

def main():
    config = load_config()
    url = config['epg']['url']
    
    # Fetch the playlist from the URL
    songs = fetch_playlist(url)
    
    # Generate the XML
    epg_xml = generate_xml(songs, config)
    
    # Save the XML to a file
    with open(config['epg']['output_file'], 'w', encoding='utf-8') as file:
        file.write(epg_xml)

    print("EPG XML generated successfully!")

if __name__ == "__main__":
    main()
