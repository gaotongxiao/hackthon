import urllib2 as u
import re

response = u.urlopen("https://www3.aia-pt.com.hk/mpf/public/fundperf/fundchoices.jspa?lang=en_US")
res = response.read().decode("utf-8")
pattern = re.compile('<td class="col1"><a.*?>(.*?)(?:<sup>.*?</sup>)?</a>.*?center">(.*?)</td>', re.S)
items = re.findall(pattern, res)
res = {}
f = open("f.txt", "w")
for i in items:
    print(i[0], i[1])
    f.write(i[0] + "\r\n" + i[1] + "\r\n")

