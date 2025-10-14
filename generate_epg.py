import requests
from bs4 import BeautifulSoup
import yaml
from datetime import datetime

def load_config():
    with open('config.yaml', 'r') as file:
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

    return songs[:60]  # Limit to the latest 60 songs

def generate_xml(songs):
    now = datetime.now()
    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<tv date="{} +0800" generator-info-url="https://sgolden58.github.io/radio/epg.xml" source-info-url="https://sgolden58.github.io/radio/epg.xml?channel_id=988&amp;date={}">'.format(
            now.strftime("%Y%m%d%H%M%S"), now.strftime("%Y-%m-%d")),
        '<channel id="988">',
        '<display-name lang="Malaysia">988</display-name>',
        '<icon src=""/>'
    ]

    for song in songs:
        xml.append('<programme start="{}" stop="{}">'.format(
            now.strftime("%Y%m%d%H%M%S"), 
            (now + timedelta(minutes=3)).strftime("%Y%m%d%H%M%S")  # Example duration of 3 minutes
        ))
        xml.append('<title>{}</title>'.format(song['title']))
        xml.append('<desc>{}</desc>'.format(song['artist']))
        xml.append('</programme>')

    xml.append('</channel>')
    xml.append('</tv>')
    
    return "\n".join(xml)

def main():
    config = load_config()
    url = config['url']
    
    # Fetch the playlist from the URL
    songs = fetch_playlist(url)
    
    # Generate the XML
    epg_xml = generate_xml(songs)
    
    # Save the XML to a file
    with open('epg.xml', 'w', encoding='utf-8') as file:
        file.write(epg_xml)

    print("EPG XML generated successfully!")

if __name__ == "__main__":
    main()
