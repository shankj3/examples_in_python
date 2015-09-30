import urllib.parse
import urllib.request
import re

url = 'http://en.wikipedia.org/wiki/Special:Search'
values = {'search':'harvey+shank', 'go' : 'Go'}

data = urllib.parse.urlencode(values)
data = data.encode('utf-8')
req = urllib.request.Request(url, data)
resp = urllib.request.urlopen(req)

respData = resp.read()

#print(respData)

paragraphs = re.findall(r'<li>(.*?)</li>',str(respData)) 
#li is an ordered list html tag


for dup in paragraphs:
	print(dup)