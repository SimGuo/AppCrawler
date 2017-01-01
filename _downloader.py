# -*- coding:utf-8 -*-

from urllib import request
import urllib, time, requests

def download_apk(market, url, apkfile):
	if not len(url): return False
	for i in range(10):
		try:
			web = requests.get(url, stream=True)
			with open(apkfile, 'wb') as fout:
				for chunk in web.iter_content(chunk_size=204800):
					if chunk:
						fout.write(chunk)
						fout.flush()
			fout.close()
			return True
		except:
			continue
	return False
	
def download_icon(market, url, pngfile):
	if not len(url): return False
	for i in range(10):
		try:
			web = request.urlopen(url)
			data = web.read()
			File = open(pngfile, "wb")
			File.write(data)
			File.close()
			return True
		except:
			continue
	return False