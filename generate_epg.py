import datetime
import xml.etree.ElementTree as ET

# ===== CONFIG =====
CHANNEL_ID = "988"
CHANNEL_NAME = "988 FM"
CHANNEL_ICON = "https://raw.githubusercontent.com/SGolden58/svg/main/Logo/988.png"

# Replace this list with actual latest songs
songs = [
    {"title": "", "artist": ""},
]

# ===== CREATE ROOT =====
tv = ET.Element("tv")
tv.set("generator-info-name", "Radio EPG Script")
tv.set("date", datetime.datetime.now().strftime("%Y%m%d%H%M%S %z"))

# ===== CHANNEL =====
channel = ET.SubElement(tv, "channel", id=CHANNEL_ID)
display_name = ET.SubElement(channel, "display-name")
display_name.text = CHANNEL_NAME
icon = ET.SubElement(channel, "icon", src=CHANNEL_ICON)

# ===== PROGRAMMES =====
start_time = datetime.datetime.now()
song_duration = datetime.timedelta(minutes=6)  # each song 6 minutes

for song in songs:
    stop_time = start_time + song_duration
    prog = ET.SubElement(tv, "programme", channel=CHANNEL_ID)
    prog.set("start", start_time.strftime("%Y%m%d%H%M%S +0800"))
    prog.set("stop", stop_time.strftime("%Y%m%d%H%M%S +0800"))
    
    title = ET.SubElement(prog, "title", lang="zh")
    title.text = song["title"]
    
    desc = ET.SubElement(prog, "desc")
    desc.text = song["artist"]
    
    date_el = ET.SubElement(prog, "date")
    date_el.text = start_time.strftime("%Y-%m-%d")
    
    start_time = stop_time  # next song

# ===== WRITE XML =====
tree = ET.ElementTree(tv)
tree.write("epg.xml", encoding="UTF-8", xml_declaration=True)
print("EPG XML generated successfully!")
