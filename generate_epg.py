import datetime
from datetime import timezone, timedelta

# --- Timezone for Malaysia ---
tz_myt = timezone(timedelta(hours=8))
today = datetime.datetime.now(tz=tz_myt)

# --- Get this week's Monday ---
monday = today - timedelta(days=today.weekday())

# --- Programme data for Monday–Thursday (unchanged) ---
# Keep your original Monday–Thursday programme data here
mon_to_thu_programmes = [
    # (start, stop, title, desc)
    ("05:00", "05:30", "988广播剧（好剧翻叮）", "经典，值得一听再听！“好剧翻叮”为你重播988广播剧团历年来的精彩作品，用半小时戏听人生百态。"),
    ("06:00", "10:00", "早点UP 陈峰、陈毅杰和Angeline", "新一天，从《早点UP》开始！陈峰、陈毅杰和Angeline联手，为你带来国内外新闻和活力正能量。全方位探讨时事，聆听公众Call-in，让你元气满满迎接挑战！电话热线: +603 77103988｜WhatsApp: +6012-5550988｜Wechat微信：FM988_MY"),
    ("10:00", "12:30", "随十奉陪 Chrystina 黄玮萄", "《随十奉陪》以“一天发现一点”为出发点，带来旅游、保健、音乐、职场等多元话题。"),
    ("12:30", "13:00", "988广播剧", "每逢星期一至五，下午12时30分，988广播剧为你献上粤语好剧，用声音陪你走入故事的世界。"),
    ("13:00", "16:00", "活力GO Chloe和Jaydern", "午餐后困意来袭？跟着Chloe和Jaydern动起来！节目涵盖音乐、流行、生活灵感、健康与健身等热门话题。"),
    ("16:00", "19:30", "敢玩最Power Danny 温力铭, Cassey 苏颖滢, Jeff 陈浩然", "下班不无聊，《敢玩最Power》陪你玩乐学知识！"),
    ("19:00", "20:00", "988新闻线 Cynthia 陈馨蕊, Stephany 姚淑婷, Jessy 林洁昕, 黄娇萱", "每天为你整理、跟进一天里最重要的国内时事资讯。"),
    ("20:00", "22:00", "Hashtag 1+1 甯逸谦", "星期一至四 8pm-10pm，甯逸谦都会带你出发，从一个个不同时代、不同国家的角落，发现有趣故事。"),
    ("22:00", "23:59", "晚抱好时光 PM Wang 王彪民", "DJ彪民用音乐与能量陪伴大家总结一天。"),
    ("00:00", "05:00", "七个凌晨的乐章", "忙碌的生活有时会令人迷失方向忘记初衷。988一连七晚带给你七种不一样的心情。")
]

# --- Programme data for Friday ---
fri_programmes = [
    ("05:00", "05:30", "988广播剧（好剧翻叮）", "经典，值得一听再听！“好剧翻叮”为你重播988广播剧团历年来的精彩作品，用半小时戏听人生百态。"),
    ("06:00", "10:00", "早点UP 陈峰、陈毅杰和Angeline", "新一天，从《早点UP》开始！陈峰、陈毅杰和Angeline联手，为你带来国内外新闻和活力正能量。全方位探讨时事，聆听公众Call-in，让你元气满满迎接挑战！电话热线: +603 77103988｜WhatsApp: +6012-5550988｜Wechat微信：FM988_MY"),
    ("10:00", "12:30", "随十奉陪 Chrystina 黄玮萄", "《随十奉陪》以“一天发现一点”为出发点，带来旅游、保健、音乐、职场等多元话题。用温柔的声音陪伴你，聊情绪与人际关系，发现生活中的美好细节。每天十点，不见不散。"),
    ("12:30", "13:00", "988广播剧", "每逢星期一至五，下午12时30分，988广播剧为你献上粤语好剧，用声音陪你走入故事的世界。988广播剧团创立于1973年，前身为有线电台“丽的呼声”话剧组，2000年正式易名为988广播剧团。"),
    ("13:00", "16:00", "活力GO Chloe和Jaydern", "午餐后困意来袭？跟着Chloe和Jaydern动起来！节目涵盖音乐、流行、生活灵感、健康与健身等热门话题，轻松自在，活力满满，陪你度过每个下午。"),
    ("16:00", "19:30", "敢玩最Power Danny 温力铭, Cassey 苏颖滢, Jeff 陈浩然", "下班不无聊，《敢玩最Power》陪你玩乐学知识！敢做敢讲敢玩，游戏笑声不断，资讯丰富，让通勤时光变黄金。加入我们，月入“百万知识”不是梦，敢玩就最Power！"),
    ("19:00", "20:00", "988新闻线 Cynthia 陈馨蕊, Stephany 姚淑婷, Jessy 林洁昕, 黄娇萱", "每天为你整理、跟进一天里最重要的国内重要的时事资讯，以最轻松但又抽丝剥茧的角度，全面探讨这些最及时的时事课题，包括政治、经济、人文、环境与经济！"),
    ("20:00", "23:59", "大城心事 陈峰", "夜晚灯火阑珊，总有话难诉。《大城心事》陪你聆听感情、人际与生活压力，用温暖声音回应听众来电留言。夜深，心更真实。"),
    ("00:00", "06:00", "七个凌晨的乐章", "忙碌的生活有时会令人迷失方向忘记初衷，你我都有一首属于自己的主题歌,而任何的音乐都承载了你我的美好回忆。每个深夜12开始至凌晨五点,，988一连七晚带给你七种不一样的心情, 为你谱出不一样的 七个凌晨的乐章。")
]

# --- Programme data for Saturday ---
sat_programmes = [
    ("06:00", "07:00", "一天一句英Chryss(重播)", "英文不用死记硬背！让 Chrystina 用趣味俚语和实用短句，陪你一起把英语学得又轻松又上手！"),
    ("07:00", "10:00", "水滚茶靓星期六 Sean 李子昭, 沈小岚", "两位黄金贵族的周末早晨，就从一壶好茶开始。一边嘆茶，一边带你环游世界——聊旅游、谈美食、分享生活趣事，还有来自各行各业的朋友现身说法，笑料与感动交织，轻松中又带点启发。电话热线: +603 77103988｜WhatsApp: +6012-5550988｜Wechat微信：FM988_MY"),
    ("10:00", "11:00", "人生下半场 杜韩念", "人生说白了只有九百个月，说长不长，说短不短，如何要在剩下的几百个月里活出精彩、活出意义？ 每逢星期六 10am-11am，有杜韩念陪你一起，轻松地探讨人生下半场。"),
    ("11:00", "13:00", "Cyn手上路 Cynthia 陈馨蕊", "迎接孩子的到来，成为父母，是一段持续学习的旅程。不是只有父母陪孩子长大，其实孩子也在陪我们一起成长。每一次进入育儿的新阶段，父母也都在重新成为“新手”。Cynthia 馨蕊以新手妈妈的视角，打造一个分享育儿知识、好物推荐与真实经验的交流空间，陪伴每一位父母一起“Cyn”手上路。"),
    ("13:00", "15:00", "988精彩声势排行榜 Chloe 罗美云, 甯逸谦", "由听众投票决定的音乐排行榜节目！榜主Chloe和逸谦每期为你送上最新人气歌曲，看看哪首歌最受欢迎、哪位偶像声势最强！一起听歌、追榜、为你喜欢的歌手打气，每一票都由你作主！"),
    ("15:00", "17:00", "听听最溜 Stephany 姚淑婷", "富有满满 energy、power、fun 和 love 的节目，Stephany淑婷给你不一样内容的单元！ 通过音乐、智力游戏、小分享 等，让智慧像泉源一样，溜进你周六的生活！"),
    ("17:00", "18:00", "偶像来了！(重播) Chloe 罗美云, Jaydern 傅建豪", "偶像说过的一句话，可能会改变一天的心情，也可能让你更有动力！《偶像来了》带你回顾那些偶像曾经说过的金句，或许搞笑，或许励志，但一定值得你来听！今天的偶像金句，又能启发你什么呢？"),
    ("18:00", "19:00", "来点Music Fun", "一小时不间断的流行歌曲，带你沉浸在最动听的旋律中。"),
    ("19:00", "21:00", "Happy Weekend My Friend Jason潘小潘", "每个周末跟我约会吧，my friend！ 除了跟你聊生活影视what now；还有潘小潘对当下热论的奇思妙想，以大数据来给社会现象进行算命，与AI碰撞出一套未来生存指南；当然少不了音乐市场的革新与转变，一起听好歌，chill with chill guy 过上一个轻松周末。"),
    ("21:00", "22:00", "来点Music Fun", "一小时不间断的流行歌曲，带你沉浸在最动听的旋律中。"),
    ("22:00", "23:00", "温少IT脑（重播）Danny 温力铭", "温少化身IT佬，为你介绍各种好玩的产品，为你示范新奇的科技小玩意，手机或电脑的app等等。透过这些玩意让你的生活更方便更swag！ 你有什么IT问题也欢迎你发问，温少试图帮你解除你的IT烦恼！除了on air内容，也可以延伸到视频成为在线内容，带你看得更清楚、玩得更尽兴！"),
    ("23:00", "23:59", "988 Weekend 自助餐", "这个节目由 DJ Point 主持，每周邀请一位不同的 988 DJ，将他们的专属歌单精心 Remix，打造成一场节奏十足的音乐自助餐。最燃的音乐料理，专属你的周六夜晚！")
    ("00:00", "07:00", "七个凌晨的乐章", "忙碌的生活有时会令人迷失方向忘记初衷，你我都有一首属于自己的主题歌,而任何的音乐都承载了你我的美好回忆。每个深夜12开始至凌晨五点,，988一连七晚带给你七种不一样的心情, 为你谱出不一样的 七个凌晨的乐章。")
]

# --- Start building XML ---
now_str = today.strftime("%Y%m%d%H%M%S")
xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<tv date="{now_str} +0800" '
    f'generator-info-url="https://sgolden58.github.io/radio/epg.xml" '
    f'source-info-url="https://sgolden58.github.io/radio/epg.xml?channel_id=988&amp;date={today.strftime("%Y%m%d")}">',
    '<channel id="988">',
    '<display-name>988 FM</display-name>',
    '<icon src="https://raw.githubusercontent.com/SGolden58/svg/main/Logo/988.png"/>',
    '</channel>'
]

# --- Function to convert programme data to XML ---
def add_programmes(day, programmes):
    for start, stop, title, desc in programmes:
        start_dt = datetime.datetime.combine(day.date(), datetime.datetime.strptime(start, "%H:%M").time(), tzinfo=tz_myt)
        stop_dt = datetime.datetime.combine(day.date(), datetime.datetime.strptime(stop, "%H:%M").time(), tzinfo=tz_myt)
        if stop_dt <= start_dt:
            stop_dt += timedelta(days=1)
        start_str = start_dt.strftime("%Y%m%d%H%M%S %z")
        stop_str = stop_dt.strftime("%Y%m%d%H%M%S %z")
        xml.append(f'''
  <programme channel="988" start="{start_str}" stop="{stop_str}">
    <title lang="zh">{title}</title>
    <desc lang="zh">{desc}</desc>
    <category>Music</category>
    <category>Others (TV Shows)</category>
    <icon src="https://raw.githubusercontent.com/SGolden58/svg/main/Logo/988.png"/>
    <rating system="MY">
      <value>U</value>
    </rating>
  </programme>''')

# --- Add Monday–Thursday programmes ---
for day_offset in range(4):
    day = monday + timedelta(days=day_offset)
    add_programmes(day, mon_to_thu_programmes)

# --- Add Friday programmes ---
friday = monday + timedelta(days=4)
add_programmes(friday, fri_programmes)

# --- Close XML ---
xml.append("</tv>")

# --- Write epg.xml ---
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write("".join(xml))

print("✅ epg.xml generated with Monday–Thursday + Friday programmes.")
