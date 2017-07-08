import urllib2 as u
import re

def getNews(keyWord="us entity"):
    print "sdasdsa"
    queryWord= keyWord.split()
    queryString="https://www.bloomberg.com/search?query="
    count = 0 
    for word in queryWord:
        if(count==0):
            queryString= queryString+ word
        else:
            queryString= queryString + "+" + word
        count = count+1
    print(queryString)
    response = u.urlopen(queryString)
    res = response.read().decode("utf-8")
    pattern = re.compile('<h1 class="search-result-story__headline">.*?href="(.*?)".*?<em>(.*?)</em>(.*?)</a>.*?</h1>', re.S)
    items = re.findall(pattern, res)
    print items
    newsList=[]

    f = open("f.txt", "w")
    for i in items:
        info =  "{links:\""+i[0]+"\",title:\""+i[1]+" "+i[2]+"\"}"
        newsList.append(info)
    print newsList    
    return newsList    
    

getNews()