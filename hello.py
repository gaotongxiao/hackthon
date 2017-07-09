from mod_python import apache, util
import json
import urllib2 as u
import re

def handler(req):
    req.content_type='application/json'
    data = req.read()
    data = json.loads(str(data))
    data = data["result"]["parameters"]
    speech = str(checkType(data))
    res = {"speech":speech, "displayText":"hihihihi", "source":"DuckDuckGo"}
    req.write(str(json.dumps(res)))
    return apache.OK

def checkType(data):
    if "expection" in data.keys():
        return getBestProduct(data)
    elif "goodChoice" in data.keys():
        if int(data["goodChoice"]) == 0:
            return compareProducts(2)
        else:
            return chooseProduct(data)
    elif "product" in data.keys():
        if int(data["product"]) == 3:
            return "I'm really sorry, see you again."
        else:
            return chooseProduct(data)
    elif "Choice" in data.keys():
        if int(data["Choice"]) == 1:
            return getRisk()
        else:
            return getNews()
            return "news"
    return "Emmm... could you please say that again?"

def riskCal(data):
    try:
        risk =  5000 * int(data["expection"]) + int(data["income"]) + 1000 * ((int(data["year"]) - 2017))
    except:
        risk = 0
    if risk < 7000:
        return 1
    elif risk < 15500:
        return 2
    elif risk < 24000:
        return 3
    elif risk < 58000:
        return 4
    return 5

def getBestProduct(data):
    risk = riskCal(data)
    fundInfo = json.loads(open("/var/www/html/FundInfo.json", "r").read(), "utf-8")
    sortList = list()
    for item in fundInfo:
        try:
            if int(item["riskRate"]) == risk:
                sortList.append(item)
        except:
            continue
    sortList = sorted(sortList, sortFuncForStar)
    temp = open("/var/www/html/sortedProducts", "w")
    temp.write(json.dumps(sortList))
    temp.close()
    bestProduct = sortList[0]
    temp = open("/var/www/html/altProducts", "w")
    temp.write(json.dumps([bestProduct]))
    temp.close()
    ret = "Name: " + bestProduct['name'] + '\r\nRisk level: ' + bestProduct['riskRate'] + ' - it matches your taste!\r\nAnnual return: ' + bestProduct['yearToDateRate'] + '%(year-to-date); ' + bestProduct['1YearRate'] + '%; ' + bestProduct['3YearRate'] + '%;\r\nCategory: ' + bestProduct['category'] + "\r\n Do you want to know more about this fund?"
    return ret

def sortFuncForStar(a, b):
    if a['star'] == 'NA':
        if b['star'] == 'NA':
            return 0
        else:
            return 1
    else:
        if b['star'] == 'NA':
            return -1
        else:
            an = int(a['star'])
            bn = int(b['star'])
            if an > bn:
                return -1
            elif an < bn:
                return 1
            else:
                if a['3YearRate'] == '-':
                    if b['3YearRate'] == '-':
                        return 0
                    else:
                        return 1
                else:
                    if b['3YearRate'] == '-' or float(b['3YearRate']) < float(a["3YearRate"]):
                        return -1
                    else:
                        return 1

def chooseProduct(data):
    altProducts = json.loads(open("/var/www/html/altProducts", "r").read())
    if int(data["product"]) > len(altProducts):
        return "Invalid input!"
    temp = open("/var/www/html/currentProduct", "w")
    temp.write(json.dumps(altProducts[int(data["product"]) - 1]))
    temp.close()
    return "What do you want to know? 1. Potential risks 2. Relative news"

def compareProducts(num):
    sortedProducts = json.loads(open("/var/www/html/sortedProducts", "r").read())
    if num > len(sortedProducts):
        return -1
    altProducts = sortedProducts[0:num]
    temp = open("/var/www/html/altProducts", "w")
    temp.write(json.dumps(altProducts))
    temp.close()
    bestProduct = sortedProducts[0]
    ret = "Check if you're interested in other products? 1. Name: " + bestProduct['name'] + '\r\nRisk level: ' + bestProduct['riskRate'] + ' - it matches your taste!\r\nAnnual return: ' + bestProduct['yearToDateRate'] + '%(year-to-date); ' + bestProduct['1YearRate'] + '%; ' + bestProduct['3YearRate'] + '%; \r\nCategory: ' + bestProduct['category']
    bestProduct = sortedProducts[1]
    ret += '\r\n' + "2. Name: " + bestProduct['name'] + '\r\nRisk level: ' + bestProduct['riskRate'] + ' - it matches your taste!\r\nAnnual return: ' + bestProduct['yearToDateRate'] + '%(year-to-date); ' + bestProduct['1YearRate'] + '%; ' + bestProduct['3YearRate'] + '%;Category: ' + bestProduct['category']
    ret += "\r\nYou may tell me your preference or just say goodbye."
    return ret


def getNews(keyWord="us entity"):
    product = json.loads(open("/var/www/html/currentProduct", "r").read())
    queryWord= keyWord.split()
    queryString="https://www.bloomberg.com/search?query="
    count = 0 
    for word in queryWord:
        if(count==0):
            queryString= queryString + word
        else:
            queryString= queryString + "+" + word
        count = count + 1
    response = u.urlopen(queryString)
    res = response.read().decode("utf-8")
    pattern = re.compile('<h1 class="search-result-story__headline">.*?href="(.*?)".*?<em>(.*?)</em>(.*?)</a>.*?</h1>', re.S)
    items = re.findall(pattern, res)
    newsList=[]

    for i in items:
        info =  "{links:\""+i[0]+"\",title:\""+i[1]+" "+i[2]+"\"}"
        newsList.append(info)
    return json.dumps(newsList)

def getRisk():
    product = json.loads(open("/var/www/html/currentProduct", "r").read())
    risks = json.loads(open("/var/www/html/risk.json","r").read(), "utf-8")
    dic = {}
    for i in risks["fund"]:
        dic.update(i)
    return dic[product['category']]
