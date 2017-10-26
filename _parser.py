# -*- coding:utf-8 -*-

import re
from bs4 import BeautifulSoup

from _unescaper import *

def get_app_basic_info(market, data):
	dict = {}
	soup = BeautifulSoup(data, "lxml")
	if market == 'yingyongbao':
		matcher = soup.find_all("div", class_ = "det-name-int")
		if len(matcher):
			dict['Name'] = unescape(matcher[0].string.replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.find_all("div", class_ = "det-ins-num")
		if len(matcher):
			dict['Download'] = unescape(matcher[0].string.replace("下载", "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.find_all("div", class_ = "det-size")
		if len(matcher):
			dict['Size'] = unescape(matcher[0].string.replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.find_all("div", class_ = "com-blue-star-num")
		if len(matcher):
			dict['Rating'] = unescape(matcher[0].string.replace("分", "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.select('#J_CommentCount')
		if len(matcher):
			dict['Rating_Num'] = unescape(matcher[0].get_text().replace("（", "").replace("）", "").replace("人评论", "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.select("#J_DetCate")
		if len(matcher):
			dict['Category'] = unescape(matcher[0].get_text().replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.select("#det-othinfo-data")
		if len(matcher) >= 2:
			dict['Edition'] = unescape(matcher[0].get_text().replace('V', "").replace('v', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
			dict['Developer'] = unescape(matcher[2].get_text(0).replace('v', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.select("#J_ApkPublishTime")
		if len(matcher):
			dict['Update_Time'] = unescape(matcher[0].get_text().replace('\t', " ").replace('\r', "").replace('\n', " "))
		if 'adv-btn_has">有广告' in data: dict['Has_Ads'] = 'True'
		elif 'adv-btn">无广告' in data: dict['Has_Ads'] = 'False'
			
	elif market == 'baidu':
		matcher = soup.select(".gray")
		if len(matcher):
			dict['Name'] = unescape(matcher[0].get_text().replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.select(".download-num")
		if len(matcher):
			dict['Download'] = unescape(matcher[0].get_text().replace("下载次数:", "").replace(" ", "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.select(".detail")
		if len(matcher):
			matcher = matcher[0].select(".size")
			if len(matcher):
				dict['Size'] = unescape(matcher[0].get_text().replace("大小:", "").replace(" ", "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.find_all("span", class_ = "star-percent")
		if len(matcher):
			dict['Rating'] = unescape(matcher[0].attrs['style'].replace("width:", "").replace("%", "").replace('\t', " ").replace('\r', "").replace('\n', " "))

		matcher = soup.select('#J_CommentCount')
		if len(matcher):
			dict['Rating_Num'] = unescape(matcher[0].get_text().replace("（", "").replace("）", "").replace("人评论", "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.find_all("a", target = "_self")
		if len(matcher) >= 3:
			type0 = unescape(matcher[1].string.replace('\t', " ").replace('\r', "").replace('\n', " "))
			type1 = unescape(matcher[2].string.replace('\t', " ").replace('\r', "").replace('\n', " "))
			dict['Category'] = type0+"-"+type1
		matcher = soup.select(".version")
		if len(matcher):
			dict['Edition'] = unescape(matcher[0].get_text().replace("版本:", "").replace(" ", "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		if '<span class="res-tag-ok">无广告</span>' in data: dict['Has_Ads'] = 'False'
		elif '<span class="res-tag-warning">含广告</span>' in data: dict['Has_Ads'] = 'True'

	elif market == '360':
		matcher = soup.select("#app-name")
		if len(matcher):
			if len(matcher[0].select('span')):
				dict['Name'] = unescape(matcher[0].select('span')[0].get_text().replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.select(".s-3")
		if len(matcher) >= 2:
			dict['Download'] = unescape(matcher[0].get_text().replace("下载：", "").replace("次", "").replace(" ", "").replace('\t', " ").replace('\r', "").replace('\n', " "))
			dict['Size'] = unescape(matcher[1].get_text().replace(" ", "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.find_all("span", class_ = "s-1 js-votepanel")
		if len(matcher):
			if len(matcher[0].contents):
				dict['Rating'] = unescape(matcher[0].contents[0].replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.find_all("span", class_ = "js-comments review-count-all")
		if len(matcher):
			if len(matcher[0].contents):
				dict['Comment_Num'] = unescape(matcher[0].string.replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.select(".review-count-best")
		if len(matcher):
			if len(matcher[0].contents):
				dict['Best_Comment_Num'] = unescape(matcher[0].string.replace('(', "").replace(')', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.select(".review-count-good")
		if len(matcher):
			if len(matcher[0].contents):
				dict['Good_Comment_Num'] = unescape(matcher[0].string.replace('(', "").replace(')', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.select(".review-count-bad")
		if len(matcher):
			if len(matcher[0].contents):
				dict['Bad_Comment_Num'] = unescape(matcher[0].string.replace('(', "").replace(')', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.select("#authority-tg")
		if len(matcher):
			matcher = re.findall('[0-9]+', matcher[0].contents[1])
			if len(matcher):
				dict['Permission_Num'] = unescape(matcher[0])
		matcher = soup.find_all("div", class_ = "app-tags")
		if len(matcher):
			matcher = soup.find_all("a", style = "color:#007fc1")
			if len(matcher):
				tagall = ""
				for line in matcher:
					tagall += line.string.replace('\t', " ").replace('\r', "").replace('\n', " ") + ";"
				dict['Tag'] = tagall[:-1]
		if '</span>有广告</li>' in data: dict['Has_Ads'] = 'True'
		elif '</span>无广告</li>' in data: dict['Has_Ads'] = 'False'
		if '</span>免费</li>' in data: dict['Free'] = 'True'
		elif '</span>含支付项</li>' in data: dict['Free'] = 'False'
		matcher = re.findall('<strong>作者：</strong>.*?<', data)
		if len(matcher): dict['Developer'] = unescape(matcher[0].replace('<strong>作者：</strong>', "").replace('<', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<strong>更新时间：</strong>.*?<', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('<strong>更新时间：</strong>', "").replace('<', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<strong>版本：</strong>.*?<', data)
		if len(matcher): dict['Edition'] = unescape(matcher[0].replace('<strong>版本：</strong>', "").replace('<', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<strong>系统：</strong>.*?<', data)
		if len(matcher): dict['System'] = unescape(matcher[0].replace('<strong>系统：</strong>', "").replace('<', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<strong>语言：</strong>.*?<', data)
		if len(matcher): dict['Language'] = unescape(matcher[0].replace('<strong>语言：</strong>', "").replace('<', "").replace('\t', " ").replace('\r', "").replace('\n', " "))

	elif market == 'googleplay':
		matcher = re.findall('<div class="id-app-title" tabindex="0">.*?</div>', data)
		if len(matcher): dict['Name'] = unescape(matcher[0].replace('<div class="id-app-title" tabindex="0">', "").replace('</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<div class="content" itemprop="numDownloads">.*?</div>', data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('<div class="content" itemprop="numDownloads">', "").replace('</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " ")).replace(' ', "")
		matcher = re.findall('<div class="content" itemprop="fileSize">.*?</div>', data)
		if len(matcher): dict['Size'] = unescape(re.subn(' *<.*?> *', "", matcher[0])[0])
		matcher = re.findall('<div class="score" aria-label=".*?">[0-9\.]+</div>', data)
		if len(matcher): dict['Rating'] = re.subn('<.*?>', "", matcher[0])[0]
		matcher = re.findall('<span class="reviews-num" aria-label=".*?">[0-9,]+</span>', data)
		if len(matcher): dict['Rating_Num'] = re.subn('<.*?>', "", matcher[0])[0].replace(",", "")
		matcher = re.findall('<span class="bar-number" aria-label=".*?">[0-9,]+</span>', data)
		if len(matcher) >= 5:
			dict['5-Star_Rating_Num'] = re.subn('<.*?>', "", matcher[0])[0].replace(",", "")
			dict['4-Star_Rating_Num'] = re.subn('<.*?>', "", matcher[1])[0].replace(",", "")
			dict['3-Star_Rating_Num'] = re.subn('<.*?>', "", matcher[2])[0].replace(",", "")
			dict['2-Star_Rating_Num'] = re.subn('<.*?>', "", matcher[3])[0].replace(",", "")
			dict['1-Star_Rating_Num'] = re.subn('<.*?>', "", matcher[4])[0].replace(",", "")
		matcher = re.findall('<span itemprop="genre">.*?</span>', data)
		if len(matcher):
			categoryall = ""
			for category in matcher:
				categoryall += unescape(category.replace('<span itemprop="genre">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))+";"
			dict['Category'] = categoryall[:-1]
		matcher = re.findall('<div class="content" itemprop="softwareVersion">.*?</div>', data)
		if len(matcher): dict['Edition'] = re.subn(' *<.*?> *', "", matcher[0])[0]
		matcher = re.findall('<span itemprop="name">.*?</span>', data)
		if len(matcher): dict['Developer'] = unescape(matcher[0].replace('<span itemprop="name">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<div class="content" itemprop="operatingSystems">.*?</div>', data)
		if len(matcher): dict['System'] = unescape(re.subn(' *<.*?> *', "", matcher[0])[0])
		matcher = re.findall('<div class="content" itemprop="datePublished">.*?</div>', data)
		if len(matcher): dict['Update_Time'] = unescape(re.subn(' *<.*?> *', "", matcher[0])[0])
		matcher = re.findall('<div class="content" itemprop="contentRating">.*?</div>', data)
		if len(matcher): dict['Age'] = unescape(re.subn(' *<.*?> *', "", matcher[0])[0])
		matcher = re.findall('</jsl> *</jsl> *<span>.*?</span> *</button>', data)
		if len(matcher): dict['Price'] = unescape(re.subn(' *<.*?> *', "", matcher[0])[0]).replace("安装", "免费").replace("Install", "Free")
		
	elif market == 'huawei':
		matcher = soup.find_all("div", class_ = "app-info flt")
		if len(matcher):
			tmpmatcher = matcher[0].select(".title")
			if len(tmpmatcher):
				dict['Name'] = unescape(tmpmatcher[0].string.replace('\t', " ").replace('\r', "").replace('\n', " "))
			tmpmatcher = matcher[0].find_all("span", class_ = "grey sub")
			if len(tmpmatcher):
				dict['Download'] = unescape(tmpmatcher[0].string.replace("下载：", "").replace("次", "").replace(" ", "").replace('\t', " ").replace('\r', "").replace('\n', " "))
			tmpmatcher = matcher[0].find_all("span", class_ = re.compile("score_"))
			if len(tmpmatcher):
				dict['Rating'] = unescape(tmpmatcher[0]["class"][0].replace("score_", "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.find_all("li", class_ = "ul-li-detail")
		if len(matcher) >= 4:
			dict['Size'] = unescape(matcher[0].find_all("span")[0].string.replace(" ", "").replace('\t', " ").replace('\r', "").replace('\n', " "))
			dict['Update_Time'] = unescape(matcher[1].find_all("span")[0].string.replace('\t', " ").replace('\r', "").replace('\n', " "))
			dict['Developer'] = unescape(matcher[2].find_all("span")[0].get("title").replace('\t', " ").replace('\r', "").replace('\n', " "))
			dict['Edition'] = unescape(matcher[3].find_all("span")[0].string.replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.find_all(class_ = "sub nofloat")
		if len(matcher):
			matcher = matcher[0].find_all("span")
			if len(matcher) and len(matcher[0].string):
				matcher = re.findall("[0-9]+", matcher[0].string)
				if len(matcher): dict['Rating_Num'] = unescape(matcher[0].replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="title flt ft-yh">.*?排行<', data)
		if len(matcher): dict['Category'] = unescape(matcher[0].replace('<span class="title flt ft-yh">', "").replace('排行<', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
	
	elif market == 'xiaomi':
		matcher = soup.select(".intro-titles")
		if len(matcher):
			matcher = matcher[0]
			tmpmatcher = matcher.select("p")
			if len(tmpmatcher):
				dict['Developer'] = unescape(tmpmatcher[0].string.replace('\t', " ").replace('\r', "").replace('\n', " "))
			tmpmatcher = matcher.select("h3")
			if len(tmpmatcher):
				dict['Name'] = unescape(tmpmatcher[0].string.replace('\t', " ").replace('\r', "").replace('\n', " "))
			tmpmatcher = matcher.find_all(class_ = "special-font action")
			if len(tmpmatcher):
				tmpmatcher = tmpmatcher[0].contents
				dict['Category'] = unescape(tmpmatcher[1].replace('\t', " ").replace('\r', "").replace('\n', " "))
				dict['Device'] = unescape(tmpmatcher[4].replace('\t', " ").replace('\r', "").replace('\n', " "))
			tmpmatcher = matcher.find_all(class_ = "star1-empty")
			if len(tmpmatcher):
				tmpmatcher = tmpmatcher[0].select("div")
				dict['Rating'] = unescape(tmpmatcher[0].get("class")[1].replace("star1-", "").replace('\t', " ").replace('\r', "").replace('\n', " "))
			tmpmatcher = matcher.find_all(class_ = "app-intro-comment")
			if len(tmpmatcher):
				tmpmatcher = re.findall("[0-9]+", tmpmatcher[0].string)
				if len(tmpmatcher): dict['Rating_Num'] = unescape(tmpmatcher[0].replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.find_all(class_ = "details preventDefault")
		if len(matcher):
			matcher = matcher[0].find_all(class_ = "cf")
			if len(matcher):
				matcher = matcher[0].find_all("li", class_ = False)
				if len(matcher) >= 3:
					dict['Size'] = unescape(matcher[0].string.replace('\t', " ").replace('\r', "").replace('\n', " "))
					dict['Edition'] = unescape(matcher[1].string.replace('\t', " ").replace('\r', "").replace('\n', " "))
					dict['Update_Time'] = unescape(matcher[2].string.replace('\t', " ").replace('\r', "").replace('\n', " "))

	elif market == 'wandoujia':
		matcher = soup.find_all(class_ = "download-wp")
		if len(matcher):
			matcher = matcher[0].find("a")
			if matcher != None:
				dict['Name'] = unescape(matcher.get("data-app-name").replace('\t', " ").replace('\r', "").replace('\n', " "))
				dict['Edition'] = unescape(matcher.get("data-app-vname").replace('\t', " ").replace('\r', "").replace('\n', " "))
				dict['Download'] = unescape(matcher.get("data-install").replace('\t', " ").replace('\r', "").replace('\n', " "))
				if matcher.get('date-like') != None: dict['Like_Num'] = unescape(matcher.get('date-like').replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.find_all("dl", class_ = "infos-list")
		if len(matcher):
			tmpmatcher = matcher[0].find_all("meta")
			if len(tmpmatcher):
				dict['Size'] = unescape(tmpmatcher[0]['content'].replace('\t', " ").replace('\r', "").replace('\n', " "))
			tmpmatcher = matcher[0].find_all(itemprop = "SoftwareApplicationCategory")
			if len(tmpmatcher) and len(tmpmatcher[0].string):
				dict['Category'] = unescape(tmpmatcher[0].string.replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.find_all(class_ = "item last comment-open")
		if len(matcher):
			matcher = matcher[0].find("i")
			if len(matcher): dict['Comment_Num'] = unescape(matcher.string.replace('\t', " ").replace('\r', "").replace('\n', " ").replace(" ", ""))
		matcher = soup.find_all(itemprop = "operatingSystems")
		if len(matcher) and len(matcher[0].contents):
			if matcher[0].contents[0].string != None:
				dict['System'] = unescape(matcher[0].contents[0].string.replace('\t', " ").replace('\r', "").replace('\n', " ").replace(" ", ""))
		matcher = soup.find_all(class_ = "side-tags clearfix")
		if len(matcher):
			matcher = matcher[0].find_all(class_ = "tag-box")
			tagall = ""
			for tag_line in matcher:
				tmptag = tag_line.find("a")
				if tmptag.string != None: tagall += unescape(tmptag.string.replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))+";"
				dict['Tag'] = tagall[:-1]
		matcher = soup.find_all(class_ = "dev-sites")
		if len(matcher) and matcher[0].string != None:
			dict['Developer']  = unescape(matcher[0].string.replace('\t', " ").replace('\r', "").replace('\n', " ").replace(" ", ""))
		matcher = soup.find_all(itemprop = "datePublished")
		if len(matcher):
			matcher = matcher[0].get("datetime")
			if matcher != None:	dict['Update_Time'] = unescape(matcher.replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		if '<s class="tag adv-embed"></s>' in data: dict['Has_Ads'] = 'True'
		elif '<s class="tag no-ad"></s>' in data: dict['Has_Ads'] = 'False'
		
	elif market == 'anzhi':

		matcher = soup.find_all(class_ = "detail_description")
		if len(matcher):
			tmpmatcher = matcher[0].find_all(class_ = "detail_line")
			if len(tmpmatcher) >= 2:
				dict['Name'] = unescape(tmpmatcher[0].find("h3").string.replace('\t', " ").replace('\r', "").replace('\n', " "))
				dict['Edition'] = unescape(tmpmatcher[0].find("span").string.replace("(", "").replace(")", "").replace('\t', " ").replace('\r', "").replace('\n', " "))
				dict['Rating'] = str(abs(int(tmpmatcher[1].find("div").get("style").replace("background-position:0 ", "").replace("px;", "").replace('\t', " ").replace('\r', "").replace('\n', " ")))/15)
		matcher = matcher[0].find(id = "detail_line_ul")
		if len(matcher):
			tmpmatcher = matcher.find_all("li")
			dict['Category'] = unescape(tmpmatcher[0].string.replace("分类：", "").replace('\t', " ").replace('\r', "").replace('\n', " "))
			dict['Download'] = unescape(tmpmatcher[1].find("span").string.replace("下载：", "").replace("+", "").replace('\t', " ").replace('\r', "").replace('\n', " "))
			dict['Update_Time'] = unescape(tmpmatcher[2].string.replace("时间：", "").replace('\t', " ").replace('\r', "").replace('\n', " "))
			dict['Size'] = unescape(tmpmatcher[3].find("span").string.replace("大小：", "").replace('\t', " ").replace('\r', "").replace('\n', " "))
			dict['System'] = unescape(tmpmatcher[4].string.replace("系统：", "").replace('\t', " ").replace('\r', "").replace('\n', " "))
			dict['Developer'] = unescape(tmpmatcher[6].string.replace("作者：","").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = soup.find_all( id = "comment_box")
		if len(matcher):
			matcher = matcher[0].find("a")
			if matcher != None and matcher.string != None:
				dict['Rating_Num'] = unescape(matcher.string.replace("评论(", "").replace(")", "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		if '<span class="spaceleft">资费：免费</span>' in data: dict['Free'] = 'True'
		
	elif market == '91':
		matcher = re.findall('<h1 class="ff f20 fb fl">.*?</h1>', data, re.S)
		if len(matcher): dict['Name'] = unescape(re.subn(' *<.*?> *', "", matcher[0].replace('\t', " ").replace('\r', "").replace('\n', ""))[0])
		matcher = re.findall('下载次数：.*?\r?\n.*?</li>', data)
		if len(matcher): dict['Download'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace("下载次数：", "").replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<li>文件大小：.*?</li>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('<li>文件大小：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="spr star"><a class="w. spr"></a></span><span class="ding spr">', data)
		if len(matcher): dict['Rating'] = matcher[0].replace('<span class="spr star"><a class="w', "").replace(' spr"></a></span><span class="ding spr">', "")
		matcher = re.findall('<span class="ding spr">.*?</span>', data, re.S)
		if len(matcher): dict['Like_Num'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<span class="cai spr">.*?</span>', data, re.S)
		if len(matcher): dict['Dislike_Num'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		_91categorydict = {
		"/game/34_1_5": "休闲娱乐", "/game/44_1_5": "竞速游戏", "/game/36_1_5": "益智游戏", "/game/35_1_5": "射击游戏", "/game/40_1_5": "策略游戏", "/game/42_1_5": "动作游戏",
		"/game/33_1_5": "角色扮演", "/game/41_1_5": "模拟经营", "/game/43_1_5": "体育竞技", "/game/39_1_5": "冒险游戏", "/game/37_1_5": "棋牌天地", "/game/53_1_5": "网络游戏",
		"/game/45_1_5": "格斗游戏", "/game/38_1_5": "情景游戏", "/soft/7_1_5": "系统工具", "/soft/18_1_5": "日常应用", "/soft/27_1_5": "影音媒体", "/soft/29_1_5": "视频软件",
		"/soft/51_1_5": "图书教育", "/soft/6_1_5": "网络应用", "/soft/2_1_5": "即时聊天", "/soft/28_1_5": "音频软件", "/soft/26_1_5": "其他工具", "/soft/48_1_5": "书籍杂志",
		"/soft/49_1_5": "社区交友", "/soft/47_1_5": "生活健康", "/soft/30_1_5": "图像处理", "/soft/17_1_5": "查询参考", "/soft/8_1_5": "系统管理", "/soft/5_1_5": "浏览辅助",
		"/soft/12_1_5": "主题美化", "/soft/16_1_5": "地图导航", "/soft/10_1_5": "安全防范", "/soft/19_1_5": "新闻阅读", "/soft/31_1_5": "照相增强", "/soft/52_1_5": "儿童教学",
		"/soft/15_1_5": "电子词典", "/soft/23_1_5": "时钟日历", "/soft/20_1_5": "理财工具", "/soft/11_1_5": "中文输入", "/soft/3_1_5": "通话辅助", "/soft/25_1_5": "名片管理",
		"/soft/22_1_5": "文档处理", "/soft/9_1_5": "文件管理", "/soft/24_1_5": "日程备忘", "/soft/4_1_5": "短信增强", "/soft/14_1_5": "词典查询", "/soft/21_1_5": "计算工具",
		"/soft/13_1_5": "蓝牙红外", "/soft/1_1_5": "网络通信"
		}
		matcher = re.findall('<a href=".*?" class="more fr">更多>></a>', data)
		if len(matcher):
			categoryid = unescape(matcher[0].replace('<a href="', "").replace('" class="more fr">更多>></a>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
			if categoryid in _91categorydict: dict['Category'] = _91categorydict[categoryid]
		matcher = re.findall('<li class="long">热门标签：.*?</li>', data, re.S)
		if len(matcher):
			matcher = re.findall('<a href=.*?>.*?</a>', matcher[0], re.S)
			if len(matcher):
				tagall = ""
				for tag in matcher:
					tagall += unescape(re.subn('<.*?>', "", tag)[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))+";"
				dict['Tag'] = tagall[:-1]
		matcher = re.findall('<li>版本：.+', data)
		if len(matcher): dict['Edition'] = unescape(matcher[0].replace('<li>版本：', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li class="long">开发商：.*?</li>', data)
		if len(matcher): dict['Developer'] = re.subn('<.*?>', "", unescape(matcher[0].replace('<li class="long">开发商：', "").replace('</li>', " ").replace('\r', "").replace('\n', " ")))[0]
		matcher = re.findall('<li>分享日期：.*?</li>', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('<li>分享日期：', "").replace('</li>', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li>适用固件：.*?</li>', data)
		if len(matcher): dict['System'] = unescape(matcher[0].replace('<li>适用固件：', "").replace('</li>', " ").replace('\r', "").replace('\n', " "))
		if '>无广告</em>' in data: dict['Has_Ads'] = 'False'
		elif '>内嵌广告</em>' in data: dict['Has_Ads'] = 'True'

	elif market == 'oppo':
		matcher = re.findall('<div class="soft_info_middle">.*?<h3>.*?</h3>', data, re.S)
		if len(matcher): dict['Name'] = unescape(re.subn(' *<.*?> *', "", matcher[0].replace('\t', " ").replace('\r', "").replace('\n', ""))[0])
		matcher = re.findall('&nbsp;&nbsp;.*?次下载', data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('&nbsp;&nbsp;', "").replace('次下载', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li>大小：.*?</li>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('<li>大小：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<div class="soft_info_nums">.*?<div class="star_[0-9]+"></div>', data, re.S)
		if len(matcher): dict['Rating'] = unescape(re.subn('<.*?>', "", matcher[0].replace('<div class="star_', "").replace('"></div>', ""))[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<span>[0-9]+</span>个评分', data)
		if len(matcher): dict['Rating_Num'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace("个评分", "").replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<li>类别：.*?</li>', data)
		if len(matcher): dict['Category'] = unescape(matcher[0].replace('<li>类别：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li>版本：.*?</li>', data)
		if len(matcher): dict['Edition'] = unescape(matcher[0].replace('<li>版本：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li>发布时间：.*?</li>', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('<li>发布时间：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(".", "-"))
		matcher = re.findall('<li>适用系统：.*?</li>', data)
		if len(matcher): dict['System'] = unescape(matcher[0].replace('<li>适用系统：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))

	elif market == 'pp':
		matcher = re.findall('<h1 class="app-title ellipsis" title=".*?">.*?</h1>', data)
		if len(matcher): dict['Name'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace('\t', " ").replace('\r', "").replace('\n', ""))
		matcher = re.findall('<div class="app-downs">.*?下载&nbsp;\|', data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('<div class="app-downs">', "").replace('下载&nbsp;|', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(" ", ""))
		matcher = re.findall('<span class="ellipsis">大[&nbsp;]*小[&nbsp;]*<strong>.*?</strong>', data)
		if len(matcher): dict['Size'] = unescape(re.subn('<.*?<strong>', "", matcher[0])[0].replace('</strong>', "").replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<div class="app-score" title="[0-9\.]+分">', data)
		if len(matcher): dict['Rating'] = unescape(matcher[0].replace('<div class="app-score" title="', "").replace('分">', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<div class="app-comment-count">[0-9]+&nbsp;人评论</div>', data)
		if len(matcher): dict['Comment_Num'] = unescape(matcher[0].replace('<div class="app-comment-count">', "").replace('&nbsp;人评论</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('</h3><div class="app-tag-list clearfix">.*?</div>', data)
		if len(matcher): dict['Tag'] = unescape(re.subn('<.*?>', "", matcher[0].replace("</a>", ";"))[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))[:-1]
		matcher = re.findall('<span class="ellipsis">版[&nbsp;]*本[&nbsp;]*<strong>.*?</strong>', data)
		if len(matcher): dict['Edition'] = unescape(re.subn('<.*?<strong>', "", matcher[0])[0].replace('</strong>', "").replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<span class="ellipsis">更新时间[&nbsp;]+<strong>.*?</strong>', data)
		if len(matcher): dict['Update_Time'] = unescape(re.subn('<.*?<strong>', "", matcher[0])[0].replace('</strong>', "").replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<span class="ellipsis" title=.*?>最低版本[&nbsp;]+<strong>.*?</strong>', data)
		if len(matcher): dict['System'] = unescape(re.subn('<.*?<strong>', "", matcher[0])[0].replace('</strong>', "").replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		if '<span class="icon-done safe-tag">无广告</span>' in data: dict['Has_Ads'] = 'False'

	elif market == 'sogou':
		matcher = re.findall('<p class="name">.*?</p>\n.*?<p class="stars.*/p>', data)
		if len(matcher): dict['Name'] = unescape(re.subn(' *<.*?> *', "", matcher[0].replace('\t', " ").replace('\r', "").replace('\n', ""))[0])
		matcher = re.findall('<span>.*?次下载</span>', data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('<span>', "").replace('次下载</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(" ", ""))
		matcher = re.findall('<span>大小：.*?</span>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('<span>大小：', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(" ", ""))
		matcher = re.findall('<p class="stars s[0-9]+">', data)
		if len(matcher): dict['Rating'] = unescape(matcher[0].replace('<p class="stars s', "").replace('">', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(" ", ""))
		matcher = re.findall('<label>分类：</label>.*?</td>', data, re.S)
		if len(matcher):
			matcher = re.findall('<a href=.*?</a>', matcher[0])
			if len(matcher): dict['Category'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<label>标签：</label>.*?</td>', data, re.S)
		if len(matcher):
			matcher = re.findall('<a href=.*?</a>', matcher[0])
			if len(matcher):
				tagall = ""
				for tag in matcher:
					tagall += unescape(re.subn('<.*?>', "", tag)[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))+";"
				dict['Tag'] = tagall[:-1]
		matcher = re.findall('<label>版本：</label>.*?</td>', data)
		if len(matcher): dict['Edition'] = unescape(matcher[0].replace('<label>版本：</label>', "").replace('</td>', "").replace('\t', "").replace('\r', "").replace('\n', " ").replace(" ", ""))
		matcher = re.findall('<label>更新时间：</label>.*?</td>', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('<label>更新时间：</label>', "").replace('</td>', "").replace('\t', "").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<label>作者：</label>.*?</td>', data)
		if len(matcher): dict['Developer'] = unescape(matcher[0].replace('<label>作者：</label>', "").replace('</td>', "").replace('\t', "").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<label>平台：</label>.*?</td>', data)
		if len(matcher): dict['System'] = unescape(matcher[0].replace('<label>平台：</label>', "").replace('</td>', "").replace('\t', "").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<label>语言：</label>.*?</td>', data)
		if len(matcher): dict['Language'] = unescape(matcher[0].replace('<label>语言：</label>', "").replace('</td>', "").replace('\t', "").replace('\r', "").replace('\n', " ").replace(" ", ""))
		if '<span>免费</span>' in data: dict['Free'] = 'True'
		if '<span>有广告</span>' in data: dict['Has_Ads'] = 'True'
		elif '<span>无广告</span>' in data: dict['Has_Ads'] = 'False'

	elif market == 'gfan':
		matcher = re.findall('<h4 class="curr-tit">.*?</h4>', data)
		if len(matcher): dict['Name'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace('\t', " ").replace('\r', "").replace('\n', ""))
		matcher = re.findall('<span class="fl">热度</span>.*?</p>', data)
		if len(matcher):
			matcher = re.findall('<i></i>', matcher[0])
			dict['Download'] = str(len(matcher))
		matcher = re.findall('<p>文件大小：.*?</p>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('<p>文件大小：', "").replace('</p>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<i class="marking png" style=".*?"></i>.*?</span>', data)
		if len(matcher): dict['Rating'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<span class="marking-tips">[0-9]+次评分', data)
		if len(matcher): dict['Rating_Num'] = unescape(matcher[0].replace('<span class="marking-tips">', "").replace('次评分', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<h3 class="curr-site">.+&gt;.+', data)
		if len(matcher): dict['Category'] = unescape(re.subn('\(.*?\)', "", re.subn('<.*?>', "", matcher[0].split(';')[-1])[0])[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<p>版 本 号：.*?</p>', data)
		if len(matcher): dict['Edition'] = unescape(matcher[0].replace('<p>版 本 号：', "").replace('</p>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<p>发布时间：.*?</p>', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('<p>发布时间：', "").replace('</p>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<p>开 发 者：.*?</p>', data)
		if len(matcher): dict['Developer'] = unescape(matcher[0].replace('<p>开 发 者：', "").replace('</p>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<p>支持固件：.*?</p>', data)
		if len(matcher): dict['System'] = unescape(matcher[0].replace('<p>支持固件：', "").replace('</p>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(' ', ""))

	elif market == 'meizu':
		matcher = re.findall('<div class="detail_top">\n.*?<h3>.*?</h3>', data)
		if len(matcher): dict['Name'] = unescape(re.findall('<h3>.*?</h3>', matcher[0])[0].replace('<h3>', "").replace('</h3>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<div class="app_content"><span>.*?</span></div>', data)
		if len(matcher): dict['Download'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('小：</span>\n.*?<div class="app_content">\n.*?\n', data)
		if len(matcher): dict['Size'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace('小：', "").replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall(' data-num="[0-9]+"></div></div>', data)
		if len(matcher): dict['Rating'] = unescape(matcher[0].replace(' data-num="', "").replace('"></div></div>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall(' href="javascript:void\(0\)">[0-9]+', data)
		if len(matcher):
			maxpagenum = int(matcher[-1].replace(' href="javascript:void(0)">', ""))
			matcher = re.findall(' href="javascript:void\(0\)" rno="[0-9]+', data)
			if len(matcher): maxpagenum = int(matcher[0].replace(' href="javascript:void(0)" rno="', ""))
			dict['Comment_Num'] = dict['Rating_Num'] = str(maxpagenum*10)
		elif '<div id="eva">暂无评论</div>' in data:
			dict['Comment_Num'] = dict['Rating_Num'] = '0'
		else:
			matcher = re.findall('<div class="user_comment"><ul><li>', data)
			if len(matcher): dict['Comment_Num'] = dict['Rating_Num'] = str(len(matcher))
		matcher = re.findall('<div class="app_content">.*?</a></div>', data)
		if len(matcher): dict['Category'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<div class="app_content ellipsis noPointer">.*?</div>', data)
		if len(matcher): dict['Edition'] = unescape(matcher[0].replace('<div class="app_content ellipsis noPointer">', "").replace('</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<div class="app_content">[0-9\-]+</div>', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('<div class="app_content">', "").replace('</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<div class="app_content ellipsis">\n.*?\n.*?</div>', data)
		if len(matcher): dict['Developer'] = unescape(re.subn(' *<.*?> *', "", matcher[0].replace('\t', " ").replace('\r', "").replace('\n', ""))[0])
		matcher = re.findall('本：</span>\n.*?<div class="app_content">\n.*?\n', data)
		if len(matcher): dict['System'] = unescape(re.subn(' *<.*?> *', "", matcher[0].replace('\t', " ").replace('\r', "").replace('\n', ""))[0].replace('本：', ""))

	elif market == 'sina':
		matcher = re.findall('<h1 class="avName">.*?</h1>', data)
		if len(matcher): dict['Name'] = unescape(matcher[0].replace('<h1 class="avName">', "").replace('</h1>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="downValue">下载 \(.*?\)</span>', data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('<span class="downValue">下载 (', "").replace(')</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li class="avInfoItem">大小：.*?</li>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('<li class="avInfoItem">大小：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="rateStarM rateStarM-[0-9]">', data)
		if len(matcher): dict['Rating'] = unescape(matcher[0].replace('<span class="rateStarM rateStarM-', "").replace('">', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="voteValue">\([0-9]+\)</span>', data)
		if len(matcher): dict['Rating_Num'] = unescape(matcher[0].replace('<span class="voteValue">(', "").replace(')</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="meta">\([0-9]+条\)</span>', data)
		if len(matcher): dict['Comment_Num'] = unescape(matcher[0].replace('<span class="meta">(', "").replace('条)</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('secondcat=[0-9]+&">.*?</a>', data)
		if len(matcher): dict['Category'] = unescape(re.subn('.+>', "", matcher[0].replace('</a>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))[0])
		matcher = re.findall('<li class="avInfoItem">版本：.*?</li>', data)
		if len(matcher): dict['Edition'] = unescape(matcher[0].replace('<li class="avInfoItem">版本：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li class="avInfoItem">更新时间：.*?</li>', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('<li class="avInfoItem">更新时间：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li class="avInfoItem">系统要求：.*?</li>', data)
		if len(matcher): dict['System'] = unescape(matcher[0].replace('<li class="avInfoItem">系统要求：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))

	elif market == 'dcn':
		matcher = re.findall('<h1.*?</h1>', data)
		if len(matcher): dict['Name'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace('\t', " ").replace('\r', "").replace('\n', ""))
		matcher = re.findall('<span>热度</span>[0-9]+℃', data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('<span>热度</span>', "").replace('℃', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li><span>大小</span>.*?</li>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('<li><span>大小</span>', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="star star-light stars-[0-9]"></span>', data)
		if len(matcher): dict['Rating'] = unescape(matcher[0].replace('<span class="star star-light stars-', "").replace('"></span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('已有<em id="comNum2">[0-9]+</em>人发表评论</span>', data)
		if len(matcher): dict['Comment_Num'] = unescape(matcher[0].replace('已有<em id="comNum2">', "").replace('</em>人发表评论</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="de-co-num" id="coNum">\n.*?\n.*?</span>', data)
		if len(matcher):
			matcher = re.findall('[0-9]+', matcher[0])
			if len(matcher): dict['Like_Num'] = matcher[0]
		matcher = re.findall('<li.*?<span>类别</span>\n.*?\n.*?</li>', data)
		if len(matcher): dict['Category'] = unescape(re.subn('<.*?>', "", matcher[0].replace('<span>类别</span>', ''))[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(' ', ""))
		matcher = re.findall('<div class="de-tag-wrap clear module-tit-r">.*?</div>', data, re.S)
		if len(matcher):
			matcher = re.findall('<span>.*?</span>', matcher[0])
			if len(matcher):
				tagall = ""
				for tag in matcher:
					tagall += ';'+tag.replace('<span>', "").replace('</span>', "")
				dict['Tag'] = tagall[1:]
		matcher = re.findall('<li><span>版本</span><span class="ov">.*?</span></li>', data)
		if len(matcher): dict['Edition'] = unescape(matcher[0].replace('<li><span>版本</span><span class="ov">', "").replace('</span></li>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(' ', ""))
		matcher = re.findall('<li><span>时间</span>.*?</li>', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('<li><span>时间</span>', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(' ', ""))
		matcher = re.findall('<li class="clear de-game-firm">.*?<span>开发商</span>.*?</li>', data, re.S)
		if len(matcher): dict['Developer'] = unescape(re.subn(' *<.*?> *', "", matcher[0].replace('<span>开发商</span>', '').replace('\t', " ").replace('\r', "").replace('\n', ""))[0])
		matcher = re.findall('<li class="">\n.*?<span>支持系统</span>\n.*?\n.*?</li>', data)
		if len(matcher): dict['System'] = unescape(re.subn('<.*?>', "", matcher[0].replace('<span>支持系统</span>', ''))[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(' ', ""))
		matcher = re.findall('<li class="" style="float:right"><span>语言</span>.*?</li>', data)
		if len(matcher): dict['Language'] = unescape(matcher[0].replace('<li class="" style="float:right"><span>语言</span>', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(' ', ""))
		if '<li><span>资费</span>完全免费</li>' in data: dict['Free'] = 'True'
		elif '<li><span>资费</span>道具收费</li>' in data: dict['Free'] = 'False'
		if '<i class="no-ad"></i>无广告' in data: dict['Has_Ads'] = 'False'
		elif '<i class="has-ad"></i>有广告' in data: dict['Has_Ads'] = 'True'

	elif market == 'liqucn':
		soup = BeautifulSoup(data, 'lxml')
		edition = soup.find_all("div", class_ = "app_leftinfo")
		if len(edition):
			edition = edition[0].find_all("span")
			if len(edition):
				edition = edition[0].string
				if len(edition) > 2:
					dict['Edition'] = edition[3:]
		matcher = re.findall('<h3>.*?</h3><p>', data)
		if len(matcher): dict['Name'] = unescape(matcher[0].replace('<h3>', "").replace('</h3><p>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('下载次数：<em>.*?</em>', data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('下载次数：<em>', "").replace('</em>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(' ', ""))
		matcher = re.findall('文件大小：<em>.*?</em>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('文件大小：<em>', "").replace('</em>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(' ', ""))
		matcher = re.findall('类型：<em>.*?</em>', data)
		if len(matcher): dict['Category'] = unescape(matcher[0].replace('类型：<em>', "").replace('</em>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(' ', ""))
		matcher = re.findall('<h1>.*?</h1>', data)
		if len(matcher) and 'Name' in dict: dict['Edition'] = unescape(matcher[0].replace('<h1>', "").replace('</h1>', "").replace('<em class="app_gf">官方</em>', "").replace(dict['Name'], "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(' ', ""))
		matcher = re.findall('更新：<em>.*?</em>', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('更新：<em>', "").replace('</em>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(' ', ""))
		matcher = re.findall('开发商：<em>.*?</em>', data)
		if len(matcher): dict['Developer'] = unescape(matcher[0].replace('开发商：<em>', "").replace('</em>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))

	elif market == 'appchina':
		matcher = re.findall('<h1 class="app-name">.*?</h1>', data)
		if len(matcher): dict['Name'] = unescape(matcher[0].replace('<h1 class="app-name">', "").replace('</h1>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<p class="art-content">大小：.*?</p>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('<p class="art-content">大小：', "").replace('</p>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<p class="art-content">分类：.*?</p>', data)
		if len(matcher): dict['Category'] = unescape(matcher[0].replace('<p class="art-content">分类：', "").replace('</p>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<p class="art-content">版本：.*?</p>', data)
		if len(matcher): dict['Edition'] = unescape(matcher[0].replace('<p class="art-content">版本：', "").replace('</p>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<p class="art-content">更新：.*?</p>', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('<p class="art-content">更新：', "").replace('</p>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<p class="art-content">要求：.*?</p>', data)
		if len(matcher): dict['System'] = unescape(matcher[0].replace('<p class="art-content">要求：', "").replace('</p>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="app-statistic">[0-9]+人评论</span>', data)
		if len(matcher): dict['Comment_Num'] = unescape(matcher[0].replace('<span class="app-statistic">', "").replace('人评论</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('good_4.png">[0-9]+</img>', data)
		if len(matcher): dict['Like_Num'] = unescape(matcher[0].replace('good_4.png">', "").replace('</img>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('bad_4.png">[0-9]+</img>', data)
		if len(matcher): dict['Dislike_Num'] = unescape(matcher[0].replace('bad_4.png">', "").replace('</img>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		if '<span>无广告</span>' in data: dict['Has_Ads'] = 'False'
		elif '<span>有广告</span>' in data: dict['Has_Ads'] = 'True'
		if '<span>中文</span>' in data: dict['Language'] = '中文'
		elif '<span>英文</span>' in data: dict['Language'] = '英文'

	elif market == '10086':
		matcher = re.findall('<span title=".*?">.*?</span>', data)
		if len(matcher): dict['Name'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace('\t', " ").replace('\r', "").replace('\n', ""))
		matcher = re.findall('<span style="font-size:14px;"><span style="color:#ff5a00;">.*?</span>感兴趣', data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('<span style="font-size:14px;"><span style="color:#ff5a00;">', "").replace('</span>感兴趣', "").replace('<', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li>大　　小：.*?</li>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('<li>大　　小：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li>所属类别：.*?</li>', data)
		if len(matcher): dict['Category'] = unescape(matcher[0].replace('<li>所属类别：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li>版　　本：.*?</li>', data)
		if len(matcher): dict['Edition'] = unescape(matcher[0].replace('<li>版　　本：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li>更新时间：.*?</li>', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('<li>更新时间：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li> *开 发 者：.*?\n?.*?</li>', data)
		if len(matcher): dict['Developer'] = unescape(re.subn(' *<.*?> *', "", matcher[0].replace("开 发 者：", "").replace('\t', " ").replace('\r', "").replace('\n', ""))[0])
		matcher = re.findall('<li>系统支持：.*?</li>', data)
		if len(matcher): dict['System'] = unescape(matcher[0].replace('<li>系统支持：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li>价　　钱：\r?\n?.*?</li>', data)
		if len(matcher): dict['Price'] = unescape(matcher[0].replace('<li>价　　钱：', "").replace('</li>', "").replace('\t', "").replace('\r', "").replace('\n', ""))
		matcher = re.findall('喜欢：<span id="l_num">[0-9]+', data)
		if len(matcher): dict['Like_Num'] = unescape(matcher[0].replace('喜欢：<span id="l_num">', "").replace('\t', "").replace('\r', "").replace('\n', ""))

	elif market == 'lenovo':
		matcher = re.findall('<h1 class="f18 fl">.*?</h1>', data)
		if len(matcher): dict['Name'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace('\t', " ").replace('\r', "").replace('\n', ""))
		matcher = re.findall('<span class="fgrey5">下载：.*?次安装</span></div>', data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('<span class="fgrey5">下载：', "").replace('次安装</span></div>', "").replace('大于', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('大小：<span class="fgrey5">.*?</span>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('大小：<span class="fgrey5">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<p class="f20 ff-arial scoreTxt fb">.*?</p>', data)
		if len(matcher): dict['Rating'] = unescape(matcher[0].replace('<p class="f20 ff-arial scoreTxt fb">', "").replace('</p>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<p class="f16 ff-wryh fgrey5 userTotal"><var>[0-9]+</var>', data)
		if len(matcher): dict['Rating_Num'] = unescape(matcher[0].replace('<p class="f16 ff-wryh fgrey5 userTotal"><var>', "").replace('</var>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<var class="fgrey1">[0-9]+%</var>', data)
		if len(matcher) == 5:
			dict['5-Star_Rating_Num'] = unescape(matcher[0].replace('<var class="fgrey1">', "").replace('%</var>', "").replace('\t', "").replace('\r', "").replace('\n', "").replace(" ", ""))
			dict['4-Star_Rating_Num'] = unescape(matcher[1].replace('<var class="fgrey1">', "").replace('%</var>', "").replace('\t', "").replace('\r', "").replace('\n', "").replace(" ", ""))
			dict['3-Star_Rating_Num'] = unescape(matcher[2].replace('<var class="fgrey1">', "").replace('%</var>', "").replace('\t', "").replace('\r', "").replace('\n', "").replace(" ", ""))
			dict['2-Star_Rating_Num'] = unescape(matcher[3].replace('<var class="fgrey1">', "").replace('%</var>', "").replace('\t', "").replace('\r', "").replace('\n', "").replace(" ", ""))
			dict['1-Star_Rating_Num'] = unescape(matcher[4].replace('<var class="fgrey1">', "").replace('%</var>', "").replace('\t', "").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('class="fblue orange">.*?</a>', data)
		if len(matcher): dict['Category'] = unescape(matcher[-1].replace('class="fblue orange">', "").replace('</a>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('版本：<span class="fgrey5">.*?</span>', data)
		if len(matcher): dict['Edition'] = unescape(matcher[0].replace('版本：<span class="fgrey5">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('开发者：<span class="fgrey5">.*?</span>', data)
		if len(matcher): dict['Developer'] = unescape(matcher[0].replace('开发者：<span class="fgrey5">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('更新时间：<span class="fgrey5">.*?</span>', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('更新时间：<span class="fgrey5">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('适用系统：<span class="fgrey5">.*?</span>', data)
		if len(matcher): dict['System'] = unescape(matcher[0].replace('适用系统：<span class="fgrey5">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))

	elif market == 'zol':
		matcher = re.findall('<h1 class="soft-title">.*?</h1>', data)
		if len(matcher): dict['Name'] = unescape(matcher[0].replace('<h1 class="soft-title">', "").replace('</h1>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span>[0-9,]+次</span>', data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('<span>', "").replace('次</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(',', ""))
		matcher = re.findall('</span></span><em>[0-9\.]+</em></div>', data)
		if len(matcher): dict['Rating'] = unescape(matcher[0].replace('</span></span><em>', "").replace('</em></div>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('class="join-num">共 <em>[0-9]+</em> 人参与</a>', data)
		if len(matcher): dict['Rating_Num'] = dict['Comment_Num'] = unescape(matcher[0].replace('class="join-num">共 <em>', "").replace('</em> 人参与</a>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span>分类：</span>.*?</a>', data)
		if len(matcher): dict['Category'] = unescape(re.subn('<.*?>', "", matcher[0].replace('<span>分类：</span>', ""))[0].replace('\t', " ").replace('\r', "").replace('\n', ""))
		matcher = re.findall('<span>更新：</span><em>.*?</em>', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('<span>更新：</span><em>', "").replace('</em>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span>厂商：</span>.*?</em>', data)
		if len(matcher): dict['Developer'] = unescape(re.subn('<.*?>', "", matcher[0].replace('<span>厂商：</span>', ""))[0].replace('\t', " ").replace('\r', "").replace('\n', ""))
		matcher = re.findall('系统要求：</span>Android.*?</li>', data)
		if len(matcher): dict['System'] = unescape(matcher[0].replace('系统要求：</span>', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="good".*?>[0-9]+</span>', data)
		if len(matcher): dict['Like_Num'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace('\t', " ").replace('\r', "").replace('\n', ""))
		matcher = re.findall('<span class="bad".*?>[0-9]+</span>', data)
		if len(matcher): dict['Dislike_Num'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace('\t', " ").replace('\r', "").replace('\n', ""))
		matcher = re.findall('<span>语言：</span>.*?</em>', data)
		if len(matcher): dict['Language'] = unescape(re.subn('<.*?>', "", matcher[0].replace('<span>语言：</span>', ""))[0].replace('\t', " ").replace('\r', "").replace('\n', ""))

	elif market == 'nduo':
		matcher = re.findall('<h1 class="app-title ellipsis".*?>.*?</h1>', data)
		if len(matcher): dict['Name'] = unescape(re.subn(' *<.*?> *', "", matcher[0])[0].replace('\t', " ").replace('\r', "").replace('\n', ""))
		matcher = re.findall('下&nbsp;&nbsp;载&nbsp;&nbsp;量&nbsp;&nbsp;&nbsp;&nbsp;<strong>.*?</strong>', data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('下&nbsp;&nbsp;载&nbsp;&nbsp;量&nbsp;&nbsp;&nbsp;&nbsp;<strong>', "").replace('</strong>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('大&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;小&nbsp;&nbsp;&nbsp;&nbsp;<strong>.*?</strong>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('大&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;小&nbsp;&nbsp;&nbsp;&nbsp;<strong>', "").replace('</strong>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('更新时间&nbsp;&nbsp;&nbsp;&nbsp;<strong>.*?</strong>', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('更新时间&nbsp;&nbsp;&nbsp;&nbsp;<strong>', "").replace('</strong>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('版&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;本&nbsp;&nbsp;&nbsp;&nbsp;<strong>.*?</strong>', data)
		if len(matcher): dict['Edition'] = unescape(matcher[0].replace('版&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;本&nbsp;&nbsp;&nbsp;&nbsp;<strong>', "").replace('</strong>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))

	elif market == 'cnmo':
		matcher = re.findall('<p class="reviewHdConTit">.*?</p>', data)
		if len(matcher): dict['Name'] = unescape(re.subn(' *<.*?> *', "", matcher[0])[0].replace('\t', " ").replace('\r', "").replace('\n', ""))
		matcher = re.findall('<li>应用大小：.*?</li>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('<li>应用大小：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(' ', ""))
		matcher = re.findall('<div class="scores fL">[0-5]分</div>', data)
		if len(matcher): dict['Rating'] = unescape(matcher[0].replace('<div class="scores fL">', "").replace('分</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(' ', ""))
		matcher = re.findall('已有<span class="colC00">[0-9]+</span>条点评', data)
		if len(matcher): dict['Rating_Num'] = dict['Comment_Num'] = unescape(matcher[0].replace('已有<span class="colC00">', "").replace('</span>条点评', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<div class="comTotalMen">\r?\n?.*?[0-9]+人', data)
		if len(matcher) == 5:
			dict['5-Star_Rating_Num'] = unescape(re.findall('[0-9]+', matcher[0])[-1])
			dict['4-Star_Rating_Num'] = unescape(re.findall('[0-9]+', matcher[1])[-1])
			dict['3-Star_Rating_Num'] = unescape(re.findall('[0-9]+', matcher[2])[-1])
			dict['2-Star_Rating_Num'] = unescape(re.findall('[0-9]+', matcher[3])[-1])
			dict['1-Star_Rating_Num'] = unescape(re.findall('[0-9]+', matcher[4])[-1])
		matcher = re.findall('<li>应用分类：.*?</a></li>', data)
		if len(matcher): dict['Category'] = unescape(re.subn(' *<.*?> *', "", matcher[0].replace('<li>应用分类：', ""))[0].replace('\t', " ").replace('\r', "").replace('\n', ""))
		matcher = re.findall('<li>版本：.*?</li>', data)
		if len(matcher): dict['Edition'] = unescape(matcher[0].replace('<li>版本：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li>更新时间：.*?</li>', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('<li>更新时间：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li>开发厂商：.*?</li>', data)
		if len(matcher): dict['Developer'] = unescape(matcher[0].replace('<li>开发厂商：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li>运行环境：.*?</li>', data)
		if len(matcher): dict['System'] = unescape(matcher[0].replace('<li>运行环境：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li>语言：.*?</li>', data)
		if len(matcher): dict['Language'] = unescape(matcher[0].replace('<li>语言：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		if '<li>应用价格：<img src="http://icon.cnmo-img.com.cn/app/indeximg/mianfei.jpg"' in data: dict['Free'] = 'True'

	elif market == 'pconline':
		if not 'Android下载</a>' in data: return dict
		matcher = re.findall('target="_self" title=".*?下载">.*?下载</a>', data)
		if len(matcher): dict['Name'] = unescape(re.subn('下载">.*?下载</a>', "", matcher[0])[0].replace('target="_self" title="', "").replace('\t', " ").replace('\r', "").replace('\n', ""))
		matcher = re.findall('<em id="span_dl_count">[0-9]+</em>', data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('<em id="span_dl_count">', "").replace('</em>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(' ', ""))
		matcher = re.findall('软件大小： </span>.*?</li>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('软件大小： </span>', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(' ', ""))
		matcher = re.findall('</span><i class="stars"><span style="width:[0-9]+%">', data)
		if len(matcher): dict['Rating'] = unescape(matcher[0].replace('</span><i class="stars"><span style="width:', "").replace('%">', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(' ', ""))
		matcher = re.findall('评论<em class="cmtDetail">[0-9]+</em>', data)
		if len(matcher): dict['Comment_Num'] = unescape(matcher[0].replace('评论<em class="cmtDetail">', "").replace('</em>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(' ', ""))
		matcher = re.findall('<span id="JvotePos">[0-9]+</span>', data)
		if len(matcher): dict['Like_Num'] = unescape(matcher[0].replace('<span id="JvotePos">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(' ', ""))
		matcher = re.findall('<span id="JvoteNeg">[0-9]+</span>', data)
		if len(matcher): dict['Dislike_Num'] = unescape(matcher[0].replace('<span id="JvoteNeg">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(' ', ""))
		matcher = re.findall('[^<^>]*?</a> &gt; <a href="http://dl.pconline.com.cn/download/', data)
		if len(matcher): dict['Category'] = unescape(matcher[0].replace('</a> &gt; <a href="http://dl.pconline.com.cn/download/', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(' ', ""))
		matcher = re.findall('<h1>.*?</h1>', data)
		if len(matcher):
			matcher = re.findall(' [0-9\.]+ ?<?', matcher[0])
			if len(matcher): dict['Edition'] = re.findall('[0-9\.]+', matcher[-1])[0]
		matcher = re.findall('更新时间： </span>.*?</li>', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('更新时间： </span>', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li title=".*?"><span class="sub">软件厂商：', data)
		if len(matcher): dict['Developer'] = unescape(matcher[0].replace('<li title="', "").replace('"><span class="sub">软件厂商：', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		if '软件授权： </span>免费</li>' in data: dict['Free'] = 'True'
		elif '软件授权： </span>收费</li>' in data: dict['Free'] = 'False'
		matcher = re.findall('软件语言： </span>.*?</li>', data)
		if len(matcher): dict['Language'] = unescape(matcher[0].replace('软件语言： </span>', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))

	elif market == 'appcool':
		matcher = re.findall('<h1 class="det-title">.*?</h1>', data)
		if len(matcher): dict['Name'] = unescape(matcher[0].replace('<h1 class="det-title">', "").replace('</h1>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li class="fl">下载次数：.*?次</li>', data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('<li class="fl">下载次数：', "").replace('次</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li class="fl">文件大小：.*?</li>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('<li class="fl">文件大小：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<b>[0-9\.]+星</b><br />', data)
		if len(matcher): dict['Rating'] = unescape(matcher[0].replace('<b>', "").replace('星</b><br />', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<p class="f14">[0-9]+ 人评分</p>', data)
		if len(matcher): dict['Rating_Num'] = unescape(matcher[0].replace('<p class="f14">', "").replace(' 人评分</p>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('</em></span><span class="fr">[0-9]+</span></li>', data)
		if len(matcher) == 5:
			dict['5-Star_Rating_Num'] = unescape(matcher[0].replace('</em></span><span class="fr">', "").replace('</span></li>', "").replace('\t', "").replace('\r', "").replace('\n', "").replace(" ", ""))
			dict['4-Star_Rating_Num'] = unescape(matcher[1].replace('</em></span><span class="fr">', "").replace('</span></li>', "").replace('\t', "").replace('\r', "").replace('\n', "").replace(" ", ""))
			dict['3-Star_Rating_Num'] = unescape(matcher[2].replace('</em></span><span class="fr">', "").replace('</span></li>', "").replace('\t', "").replace('\r', "").replace('\n', "").replace(" ", ""))
			dict['2-Star_Rating_Num'] = unescape(matcher[3].replace('</em></span><span class="fr">', "").replace('</span></li>', "").replace('\t', "").replace('\r', "").replace('\n', "").replace(" ", ""))
			dict['1-Star_Rating_Num'] = unescape(matcher[4].replace('</em></span><span class="fr">', "").replace('</span></li>', "").replace('\t', "").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<li class="fl">所属分类：.*?</li>', data)
		if len(matcher): dict['Category'] = unescape(matcher[0].replace('<li class="fl">所属分类：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('</em>号：.*?</li>', data)
		if len(matcher): dict['Edition'] = unescape(matcher[0].replace('</em>号：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('</em>商：.*?</li>', data)
		if len(matcher): dict['Developer'] = unescape(matcher[0].replace('</em>商：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li class="fl">发布时间：.*?</li>', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('<li class="fl">发布时间：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li class="fl">支持固件：.*?</li>', data)
		if len(matcher): dict['System'] = unescape(matcher[0].replace('<li class="fl">支持固件：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(' ', ""))
		matcher = re.findall('class="mr10">.*?</a>', data)
		if len(matcher):
			tagall = ""
			for tagstr in matcher:
				tagall += ";"+unescape(tagstr.replace('class="mr10">', "").replace('</a>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
			dict['Tag'] = tagall[1:]

	return dict

def get_app_permission(market, data):
	list = []
	if market == 'yingyongbao':
		matcher = re.findall('<li class="t">需要调用以下重要权限</li>.*?</ul>', data, re.S)
		if len(matcher):
			matcher = re.findall('<div class="r">.*?</div></li>', matcher[0])
			for permission in matcher:
				list.append(unescape(permission.replace('<div class="r">', "").replace('</div></li>', "")))
				
	elif market == 'googleplay':
		matcher = re.findall('<li jstcache="[0-9]+" jsinstance="[\*0-9]+">.*?</li>', data)
		if len(matcher):
			for permission in matcher:
				list.append(unescape(re.subn('<.*?>', "", permission)[0]))
				
	elif market == 'xiaomi':
		matcher = re.findall('<li>▪ .*?</li>', data)
		if len(matcher):
			for permission in matcher:
				list.append(unescape(permission.replace('<li>▪ ', "").replace('</li>', "")))

	elif market == 'wandoujia':
		matcher = re.findall('<li><span class="perms" itemprop="permissions">.*?</span></li>', data)
		if len(matcher):
			for permission in matcher:
				list.append(unescape(permission.replace('<li><span class="perms" itemprop="permissions">', "").replace('</span></li>', "")))

	elif market == 'pp':
		matcher = re.findall('<div class="permission-list none"><p>该应用需要以下重要权限：</p><ul class="clearfix">.*?</div>', data)
		if len(matcher):
			matcher = re.findall('<li>.*?</li>', matcher[0])
			for permission in matcher:
				list.append(unescape(permission.replace('<li>', "").replace('</li>', "")))

	elif market == 'appchina':
		matcher = re.findall('<ul class="permissions-list">.*?</ul>', data, re.S)
		if len(matcher):
			matcher = re.findall('<li>.*?</li>', matcher[0])
			for permission in matcher:
				list.append(unescape(permission.replace('<li>', "").replace('</li>', "")))

	elif market == 'pconline':
		matcher = re.findall('<ul class="news new-twice-d fs-14">.*?</ul>', data, re.S)
		if len(matcher):
			matcher = re.findall('<li>.*?</li>', matcher[0])
			for permission in matcher:
				list.append(unescape(permission.replace('<li>', "").replace('</li>', "")))
	
	return tuple(set(list))
	
def get_app_description(market, data):
	if market == 'yingyongbao':
		matcher = re.findall('<div class="det-intro-tit">应用信息</div>.*?</div>[ |\n|\r|\t]*</div>', data, re.S)
		if len(matcher):
			matcher1 = re.findall('.*?<div class="det-app-data-tit">更新内容：</div>', matcher[0], re.S)
			if len(matcher1):
				tmp0 = re.subn('<.*?>', '', matcher1[0].replace('<div class="det-intro-tit">应用信息</div>', "").replace('<div class="det-app-data-tit">更新内容：</div>', "").replace('<p>', "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
				tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
				tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
				if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
				else: return tmp2
			else:
				tmp0 = re.subn('<.*?>', '', matcher[0].replace('<div class="det-intro-tit">应用信息</div>', "").replace('<p>', "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
				tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
				tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
				if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
				else: return tmp2
			
	elif market == 'baidu':
		matcher = re.findall('<div class="brief-long".*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<a href="javascript:;" target="_self" class="fold">收起</a>', "").replace('<p>', "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == '360':
		matcher = re.findall('<div class="breif">.*?<div', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<div class="breif">', "").replace('<div', "").replace('<p>', "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
			
	elif market == 'googleplay':
		matcher = re.findall('<h1 aria-label=".*?"></h1>.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<p>', "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
			
	elif market == 'huawei':
		matcher = re.findall('<div id="app_desc" style="display:none;">.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<p>', "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
	
	elif market == 'xiaomi':
		matcher = re.findall('<h3>应用介绍</h3><p class="pslide">.*?</p>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<h3>应用介绍</h3><p class="pslide">', "").replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'wandoujia':
		matcher = re.findall('<div data-originheight="100" class="con" itemprop="description">.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
			
	elif market == 'hiapk':
		matcher = re.findall('<pre id="softIntroduce">.*?</pre>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
			
	elif market == 'anzhi':
		matcher = re.findall('<div class="app_detail_title">简介：</div>.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<div class="app_detail_title">简介：</div>', "").replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
			
	elif market == '91':
		matcher = re.findall('<h3 class="h3_txt">内容介绍</h3>.*?</div>.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<h3 class="h3_txt">内容介绍</h3>', "").replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'oppo':
		matcher = re.findall('<input type="hidden" id="soft_description" value=".*?" />', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<input type="hidden" id="soft_description" value="', "").replace('" />', "").replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'pp':
		matcher = re.findall('<div class="app-detail-intro expand-panel">.*?</div>', data)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'sogou':
		matcher = re.findall('<div class="article">\n.*?<div class="textcon">\n.*?<div class="text">.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'gfan':
		matcher = re.findall('<div class="app-intro">.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', re.subn('<h5>.*?</h5>' , "", matcher[0])[0].replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'meizu':
		matcher = re.findall('应用简介：</span>.*?<div class="description_detail".*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', re.subn('应用简介：</span>' , "", matcher[0])[0].replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'sina':
		matcher = re.findall('<p id="description_p" .*?<div', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', re.subn('<div' , "", matcher[0])[0].replace('<br/>', "\n").replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'dcn':
		matcher = re.findall('<div class="de-intro-inner">.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<br/>', "\n").replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'liqucn':
		matcher = re.findall('<div class="info_brife">.*?</div>.*?<div class="p_info">.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<br/>', "\n").replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'appchina':
		matcher = re.findall('<h3>.*?</h3>.*?<p class="art-content">.*?</p>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', re.subn('<h3>.+</h3>', "", matcher[0])[0].replace('<br/>', "\n").replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == '10086':
		matcher = re.findall('<div class="mj_yyjs font-f-yh">.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<br/>', "\n").replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'lenovo':
		matcher = re.findall('<p class="f16 ff-wryh">应用简介</p>.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<p class="f16 ff-wryh">应用简介</p>', "").replace('<br/>', "\n").replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'zol':
		matcher = re.findall('<div class="text">.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[-1].replace('<p class="f16 ff-wryh">应用简介</p>', "").replace('<br/>', "\n").replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'nduo':
		matcher = re.findall('<div class="app-detail-intro expand-panel">.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<br/>', "\n").replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'cnmo':
		matcher = re.findall('<p id="conIntro".*?</p>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<br/>', "\n").replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'pconline':
		matcher = re.findall('<div class="soft-summary">.*?<[/divstrong]+>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<br/>', "\n").replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'appcool':
		matcher = re.findall('<dt>应用介绍</dt>.*?</dd>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<dt>应用介绍</dt>', "").replace('<br/>', "\n").replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	return ""
	
def get_app_release_note(market, data):
	if market == 'yingyongbao':
		matcher = re.findall('<div class="det-intro-tit">应用信息</div>.*?</div>[ |\n|\r|\t]*</div>', data, re.S)
		if len(matcher):
			matcher1 = re.findall('<div class="det-app-data-tit">更新内容：</div>.*?<div.*?[ |\n|\r|\t]*</div>', matcher[0], re.S)
			if len(matcher1):
				tmp0 = re.subn('<.*?>', '', matcher1[0].replace('<div class="det-app-data-tit">更新内容：</div>', "").replace('<br>', "\n").replace('</div>', "\n"))[0]
				tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
				tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
				if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
				else: return tmp2
				
	elif market == '360':
		matcher = re.findall('<br><b>【更新内容】</b><br>.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<br><b>【更新内容】</b><br>', "").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
			
	elif market == 'googleplay':
		matcher = re.findall('<div class="recent-change">.*?</div>', data, re.S)
		if len(matcher):
			result = ""
			for note in matcher:
				result += unescape(re.subn('<.*?>', "", note)[0].replace('<br>', "\n").replace('</div>', "\n"))+"\n"
			return result
			
	elif market == 'xiaomi':
		matcher = re.findall('<h3 class="special-h3">新版特性</h3><p class="pslide">.*?</p>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<h3 class="special-h3">新版特性</h3><p class="pslide">', "").replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
			
	elif market == 'wandoujia':
		matcher = re.findall('<div data-originheight="100" class="con">.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
	
	elif market == 'hiapk':
		matcher = re.findall('<pre class="soft_imprint_font">.*?</pre>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
			
	elif market == 'anzhi':
		matcher = re.findall('<div class="app_detail_title">更新说明：</div>.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<div class="app_detail_title">更新说明：</div>', "").replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'pp':
		matcher = re.findall('<div class="app-detail-log expand-panel">.*?</div>', data)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'meizu':
		matcher = re.findall('版本描述：</span>.*?<div class="description_detail".*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', re.subn('版本描述：</span>' , "", matcher[0])[0].replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'liqucn':
		matcher = re.findall('<h3>更新说明</h3><div class="p_info">.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<h3>更新说明</h3>' , "").replace('<p>', "\n").replace("<br/>", "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'appchina':
		matcher = re.findall('版本更新</h2>.*?<p class="art-content">.*?</p>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('版本更新</h2>' , "").replace('<p>', "\n").replace("<br/>", "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'nduo':
		matcher = re.findall('<div class="app-detail-intro expand-panelo">.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<br/>', "\n").replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'pconline':
		matcher = re.findall('更新内容</strong>.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('更新内容</strong>', "").replace('<br/>', "\n").replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'appcool':
		matcher = re.findall('<dt>新版特性</dt>.*?</dd>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<dt>新版特性</dt>', "").replace('<br/>', "\n").replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
		
	return ""
