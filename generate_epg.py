#!/usr/bin/env python3
"""
988 FM EPG Generator v3.3 - Final Implementation
"""

import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import requests
from typing import List, Dict

EPG_URL = "https://sgolden58.github.io/radio/epg.xml"
TIMEZONE_OFFSET = timedelta(hours=8)  # UTC+8

def fetch_playlist() -> List[Dict]:
    """Retrieve and parse live playlist data from specified URL"""
    try:
        response = requests.get(EPG_URL, timeout=10)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        return [
            {
                "title": prog.find('title').text.strip(),
                "artist": prog.find('artist').text.strip(),
                "duration": int(prog.find('duration').text)
            }
            for prog in root.findall('.//program')
        ][::-1]  # Reverse for chronological order
    
    except Exception as e:
        raise RuntimeError(f"Failed to fetch playlist: {str(e)}")

def generate_epg() -> str:
    """Generate EPG with millisecond-accurate timing and formatted titles"""
    base_time = datetime.utcnow() + TIMEZONE_OFFSET
    time_anchor = base_time.replace(microsecond=500000)  # Broadcast alignment
    
    tv = ET.Element("tv", 
        date=time_anchor.strftime("%Y%m%d%H%M%S"),
        generator-info-url=EPG_URL
    )
    
    # Channel configuration
    channel = ET.SubElement(tv, "channel", id="988")
    ET.SubElement(channel, "display-name", lang="zh").text = "988 FM"
    
    try:
        programs = fetch_playlist()
        current_end = time_anchor
        
        for program in programs:
            start_time = current_end - timedelta(seconds=program["duration"])
            
            programme = ET.SubElement(tv, "programme",
                channel="988",
                start=start_time.strftime("%Y%m%d%H%M%S +0800"),
                stop=current_end.strftime("%Y%m%d%H%M%S +0800")
            )
            
            # Formatted title with combined song and artist
            formatted_title = f"{program['title']} - {program['artist']}"
            ET.SubElement(programme, "title", lang="zh").text = formatted_title
            ET.SubElement(programme, "desc").text = program['artist']
            ET.SubElement(programme, "length", units="seconds").text = str(program["duration"])
            
            current_end = start_time
            
    except Exception as e:
        ET.SubElement(tv, "error").text = str(e)
    
    ET.indent(tv, space="\t")
    return ET.tostring(tv, encoding="utf-8", xml_declaration=True).decode()

if __name__ == "__main__":
    try:
        epg_xml = generate_epg()
        with open("988_epg.xml", "w", encoding="utf-8") as f:
            f.write(epg_xml)
        print(f"EPG generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
    except Exception as e:
        print(f"Critical error: {str(e)}")
