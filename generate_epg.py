from datetime import datetime, timedelta, timezone

# Malaysia timezone (+8)
tz_myt = timezone(timedelta(hours=8))

# Programme schedule (Monday–Thursday)
programmes_data = [
    ("05:00", "05:30", "988广播剧（好剧翻叮）", "经典，值得一听再听！“好剧翻叮”为你重播988广播剧团历年来的精彩作品，用半小时戏听人生百态。"),
    ("06:00", "10:00", "早点UP 陈峰、陈毅杰和Angeline", "新一天，从《早点UP》开始！陈峰、陈毅杰和Angeline联手，为你带来国内外新闻和活力正能量。"),
    ("10:00", "12:30", "随十奉陪 Chrystina 黄玮瑄", "《随十奉陪》以“一天发现一点”为出发点，带来旅游、保健、音乐、职场等多元话题。"),
    ("12:30", "13:00", "988广播剧", "下午12时30分，988广播剧为你献上粤语好剧，用声音陪你走入故事的世界。"),
    ("13:00", "16:00", "活力GO Chloe和Jaydern", "午餐后困意来袭？跟着Chloe和Jaydern动起来！节目涵盖音乐、流行、生活灵感、健康与健身等热门话题。"),
    ("16:00", "19:30", "敢玩最Power Danny 温力铭, Cassey 苏颖滢, Jeff 陈浩然", "下班不无聊，《敢玩最Power》陪你玩乐学知识！敢做敢讲敢玩，游戏笑声不断。"),
    ("19:00", "20:00", "988新闻线 Cynthia 陈馨蕊, Stephany 姚淑婷, Jessy 林洁昕, 黄娇萱", "每天为你整理、跟进一天里最重要的国内时事资讯。"),
    ("20:00", "22:00", "Hashtag 1+1 甯逸谦", "星期一至四 8pm-10pm，甯逸谦都会带你出发，从一个个不同时代、不同国家的角落，发现有趣故事。"),
    ("22:00", "23:59", "晚抱好时光 PM Wang 王彪民", "DJ彪民用音乐与能量陪伴大家总结一天。"),
    ("00:00", "05:00", "七个凌晨的乐章", "忙碌的生活有时会令人迷失方向忘记初衷。988一连七晚带给你七种不一样的心情。"),
]

# Find Monday of current week
today = datetime.now(tz_myt)
monday = today - timedelta(days=today.weekday())  # Monday = weekday 0

xml = []
logo_url = "https://raw.githubusercontent.com/SGolden58/svg/main/Logo/988.png"

# Loop Monday to Thursday only
for i in range(4):
    day = monday + timedelta(days=i)
    for start, stop, title, desc in programmes_data:
        start_dt = datetime.combine(day.date(), datetime.strptime(start, "%H:%M").time(), tz_myt)
        stop_dt = datetime.combine(day.date(), datetime.strptime(stop, "%H:%M").time(), tz_myt)
        if stop_dt <= start_dt:
            stop_dt += timedelta(days=1)
        start_str = start_dt.strftime("%Y%m%dT%H%M%S %z")
        stop_str = stop_dt.strftime("%Y%m%dT%H%M%S %z")

        xml.append(f"""
  <programme channel="988" start="{start_str}" stop="{stop_str}">
    <title>{title}</title>
    <desc>{desc}</desc>
    <category>Radio</category>
    <icon src="{logo_url}" />
  </programme>""")

output = f"""<?xml version="1.0" encoding="UTF-8"?>
<tv generator-info-name="GitHub EPG Generator">
{''.join(xml)}
</tv>
"""

with open("epg.xml", "w", encoding="utf-8") as f:
    f.write(output)

print("✅ EPG (Monday–Thursday) generated successfully!")
