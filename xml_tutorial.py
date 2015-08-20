import xml.etree.ElementTree as etree
import os

file_name = 'reed.xml'
full_file = os.path.abspath(os.path.join('data', file_name))

dom = etree.parse(full_file)

courses = dom.findall('course')
for c in courses:
	title = c.find('title').text
	num = c.find('crse').text
	days = c.find('days').text

#	print('* {} [{}] {} '.format( num, days, title))

text_file = os.path.abspath(os.path.join('data','sms-20150818063128.xml'))

text = etree.parse(text_file)

root = dom.getroot()
for body in root.findall('course'):
	reg = body.find('reg_num').text
	title = body.find('title').text
