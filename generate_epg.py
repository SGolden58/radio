import requests
from bs4 import BeautifulSoup
import datetime
import html
import yaml
import os

def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

def generate_epg(songs):
    epg = []
    for song in songs:
        entry = {
            'title': song['title'],
            'description': song['artist']
        }
        epg.append(entry)
    return epg

def main():
    config = load_config()
    songs = config.get('songs', [])
    
    while True:
        epg = generate_epg(songs)
        for entry in epg:
            print(f"Title: {entry['title']}, Description: {entry['description']}")
        
        print(f"Waiting for {config['refresh_duration_minutes']} minutes to refresh...")
        time.sleep(config['refresh_duration_minutes'] * 60)  # Sleep for the specified duration

if __name__ == "__main__":
    main()

