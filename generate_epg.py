import datetime
import pytz
from xml.etree.ElementTree import Element, SubElement, ElementTree

# Malaysia timezone (UTC+8)
tz = pytz.timezone('Asia/Kuala_Lumpur')

# Define your 988 schedule (Monday–Thursday)
schedule_data = [
    ("050000", "053000", "988广播剧（好剧翻叮）",
     "经典，值得一听再听！“好剧翻叮”为你重播988广播剧团历年来的精彩作品，用半小时戏听人生百态。"),
    ("060000", "100000", "早点UP 陈峰、陈毅杰和Angeline",
     "新一天，从《早点UP》开始！陈峰、陈毅杰和Angeline联手，为你带来国内外新闻和活力正能量。"),
    ("100000", "123000", "随十奉陪 Chrystina 黄玮瑄",
     "《随十奉陪》以“一天发现一点”为出发点，带来旅游、保健、音乐、职场等多元话题。"),
    ("123000", "130000", "988广播剧",
     "下午12时30分，988广播剧为你献上粤语好剧，用声音陪你走入故事的世界。"),
    ("130000", "160000", "活力GO Chloe和Jaydern",
     "午餐后困意来袭？跟着Chloe和Jaydern动起来！节目涵盖音乐、流行、生活灵感、健康与健身等热门话题。"),
    ("160000", "193000", "敢玩最Power Danny 温力铭, Cassey 苏颖滢, Jeff 陈浩然",
     "下班不无聊，《敢玩最Power》陪你玩乐学知识！敢做敢讲敢玩，游戏笑声不断。"),
    ("190000", "200000", "988新闻线 Cynthia 陈馨蕊, Stephany 姚淑婷, Jessy 林洁昕, 黄娇萱",
     "每天为你整理、跟进一天里最重要的国内时事资讯。"),
    ("200000", "220000", "Hashtag 1+1 甯逸谦",
     "星期一至四 8pm-10pm，甯逸谦都会带你出发，从一个个不同时代、不同国家的角落，发现有趣故事。"),
    ("220000", "235900", "晚抱好时光 PM Wang 王彪民",
     "DJ彪民用音乐与能量陪伴大家总结一天。"),
    ("000000", "050000", "七个凌晨的乐章",
     "忙碌的生活有时会令人迷失方向忘记初衷。988一连七晚带给你七种不一样的心情。"),
]

# Generate XMLTV root
tv = Element("tv")

# Loop through Monday–Thursday
days = ["Monday", "Tuesday", "Wednesday", "Thursday"]
for day in days:
    for start, stop, title, desc in schedule_data:
        programme = SubElement(tv, "programme", {
            "channel": "988",
            "start": f"{day}{start} +0000",
            "stop": f"{day}{stop} +0000"
        })
        SubElement(programme, "title").text = title
        SubElement(programme, "desc").text = desc
        SubElement(programme, "category").text = "Music"
        SubElement(programme, "category").text = "Others (TV Shows)"
        SubElement(programme, "icon", {"src": "https://raw.githubusercontent.com/SGolden58/svg/main/Logo/988.png"})
        rating = SubElement(programme, "rating", {"system": "MY"})
        SubElement(rating, "value").text = "U"

# Save XML to file
tree = ElementTree(tv)
tree.write("epg.xml", encoding="utf-8", xml_declaration=True)

print("✅ EPG XML generated successfully: epg.xml")
