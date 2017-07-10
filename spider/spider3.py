#coding=utf-8
import urllib2 as u
import re
import chardet
import codecs

response = u.urlopen("http://www.hk.morningstar.com/ap/mpf/QuickRank.aspx?tab=2&sortby=Return3Year&sortorder=DESC&nsukey=D5DtUl1jdItJBCe4qcsXFfLbUi6ChWujsg8%2b1qpVOEIrG1jXBJ5TmNPT1guylJKUFAiUhJeqyPHYJXvcPjAowV4m9KxN9fjX7Sl%2bykjcQyIKfzRhWzFbqqdyD%2fs59deqBdRZ8ftGUGXkpCcKvu8Xl%2bITUnNLP7dXzYV7Nmj%2bNvH9gxUfxvFGH9BvC7qMi0ZU")
res = response.read().decode("utf-8")
print(res)
exit()
pattern = re.compile('<td class="col1">.*?<a.*?>(.*?)</a>.*?</td>.*?(?:<td.*?>.*?</td>.*?){5}<td.*?>(.*?)</td>', re.S)
items = re.findall(pattern, res)
res = {}
f = codecs.open("f2.txt", "w", "utf-8")
for i in items:
    f.write(i[0].strip().strip("\r").strip("\n") + '\r\n' + i[1].strip().strip("\r").strip("\n") + '\r\n')
    print(i[0], i[1])
