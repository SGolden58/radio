from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from xml.dom import minidom

def generate_epg():
    # Base configuration
    timezone = "+0800"
    base_time = datetime(2025, 10, 14, 19, 29, 4)  # Current system time
    
    # Sample data structure
    programs = [
        {
            "song": "去飞吧",
            "artist": "刘力扬",
            "duration": 191  # Seconds
        },
        {
            "song": "月面着陆",
            "artist": "Wolf(s) 五坚情", 
            "duration": 188
        },
        {
            "song": "What Was I Made For? (From Barbie)",
            "artist": "Billie Eilish",
            "duration": 184
        }
    ]

    # XML structure setup
    tv = ET.Element("tv", {
        "date": base_time.strftime("%Y%m%d%H%M%S") + " " + timezone,
        "generator-info-url": "https://sgolden58.github.io/radio/epg.xml"
    })
    
    channel = ET.SubElement(tv, "channel", {"id": "988"})
    ET.SubElement(channel, "display-name", {"lang": "zh"}).text = "988"
    
    # Program generation
    current_end = base_time
    for program in reversed(programs):
        start_time = current_end - timedelta(seconds=program["duration"])
        programme = ET.SubElement(tv, "programme", {
            "channel": "988",
            "start": start_time.strftime("%Y%m%d%H%M%S") + " " + timezone,
            "stop": current_end.strftime("%Y%m%d%H%M%S") + " " + timezone
        })
        
        ET.SubElement(programme, "title", {"lang": "zh"}).text = \
            f"{program['song']} + {program['artist']}"
        ET.SubElement(programme, "desc").text = program["artist"]
        ET.SubElement(programme, "length", {"units": "seconds"}).text = \
            str(program["duration"])
        
        current_end = start_time

    # XML formatting
    xml_str = ET.tostring(tv, encoding="utf-8")
    dom = minidom.parseString(xml_str)
    return dom.toprettyxml(indent="  ")

if __name__ == "__main__":
    with open("epg.xml", "w", encoding="utf-8") as f:
        f.write(generate_epg())
    print("EPG generated successfully at epg.xml")
