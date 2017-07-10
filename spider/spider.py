#coding=utf-8
import urllib2 as u
import re
import chardet
import codecs

res = open("QuickRank.html", "r")
res = res.read().replace("\n", "")
pattern = re.compile('class="msDataText"><a.*?>(.*?)</a>.*?(?:<td.*?>.*?</td>){2}<td.*?>(.*?)</td>', re.S)
items = re.findall(pattern, res)
res = {}
f = codecs.open("stars.txt", "w", "utf-8")
pattern2 = re.compile('stars(\d).gif', re.S)
for i in items:
    r = re.findall(pattern2, str(i[1]))
    if r == list():
        continue
    f.write(i[0] + '\r\n' + r[0] + '\r\n')
    print(i[0], r)
