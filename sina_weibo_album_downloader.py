#! usr/bin/python
#coding=utf-8 
import os, threading, requests, math, re, random


# Configuration Start
OID = 1005051233281285
COOKIES = "SUB=_2AkMhFc9hf8NhqwJRmPoRym_jaI9_ygvEiebDAHzsJxJjHlE47Gaj8oPkdVHDdzd9ToAkUSPIsxRx; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWM2vn1KHS_k1aSj6DvSDWv; SINAGLOBAL=7552724259118.417.1447641174437; ULV=1447691774405:2:2:2:6434341784127.688.1447691774390:1447641174455; YF-Page-G0=7f5e11c19f51c6954c5e18e40c0b1444; _s_tentry=-; Apache=6434341784127.688.1447691774390; USRANIME=usrmdinst_29"; # Your cookies.
CRAWL_PHOTOS_NUMBER = 186
# Configuration END


COOKIES = dict((l.split('=') for l in COOKIES.split('; ')))
#先创建保存图片的目录
SAVE_PATH="image"+str(OID) + "/"
if not os.path.exists(SAVE_PATH):
	os.makedirs(SAVE_PATH)
TEMP_LastMid = ""

def save_image(image_name):
	#if not os.path.isfile(SAVE_PATH + image_name):
	sina_image_url = 'http://ww1.sinaimg.cn/large/' + image_name
	response = requests.get(sina_image_url, stream=True)
	image = response.content
	try:
		print(image_name)
		with open(SAVE_PATH+image_name,"wb") as image_object:
			image_object.write(image)
			return
	except IOError:
		print("IO Error\n")
		return
	finally:
		image_object.close



def get_album_photos_url(page):
	global TEMP_LastMid
	data={
		'ajwvr':6,
		'filter':'wbphoto|||v6',
		'page': page,
		'count':20,
		'module_id':'profile_photo',
		'oid':OID,
		'uid':'',
		'lastMid':TEMP_LastMid,
		'lang':'zh-cn',
		'_t':1,
		'callback':'STK_' + str(random.randint(10000000000000, 900000000000000))
	}
	#print(data)
	#print(COOKIES)
	album_request_result = requests.get('http://photo.weibo.com/page/waterfall',  params = data, cookies = COOKIES).text
	#print(album_request.headers)
	TEMP_LastMid = re.compile(r'"lastMid":"(\d+)"').findall(album_request_result)
	print(TEMP_LastMid)
	return (re.compile(r'(\w+.png|\w+.gif|\w+.jpg)').findall(album_request_result))

if __name__ == '__main__':
	for i in range(1, int(math.ceil(CRAWL_PHOTOS_NUMBER / 20.0))):
		threads = []
		for image_name in get_album_photos_url(i):
			#save_image(image_name);
			threads.append(threading.Thread(target=save_image, args=(image_name,)))
		for t in threads:
			#t.setDaemon(True)
			t.start()
