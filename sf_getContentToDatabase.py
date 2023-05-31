import sf_pushCalculator as push
import requests
from bs4 import BeautifulSoup

def getContent(soup):
    articleData = soup.select('.r-ent')
    articles = []
    for article in articleData:
        if article.find('a') !=None:        #文章被刪除時，標題會變None，所以要加此判斷式
            title = article.find('a').text
            url = article.find('a')['href']
            url = 'https://www.ptt.cc'+url
            author = article.find('div', 'author').text
            pushAmount = article.find('div', 'nrec').text
            pushAmount = push.pushCalculator(pushAmount)    #回傳為int
            pushDate = __getPushDate(url)
            articles.append({                  #self.articles陣列存放字典資料
                'author':author,
                'title':title, 
                'push':pushAmount,  #pushAmount為int
                'pushDate':pushDate,
                'url' : url
            })
    return articles
    #準備在此存入db

# 取得發文日期, 轉成%Y-%m-%d %H:%M:%S格式, 準備存入db
def __getPushDate(url):
    cookies = {'over18':'1'}
    htmlFile = requests.get(url, cookies= cookies)
    soup = BeautifulSoup(htmlFile.text, 'lxml')
    dateStr = soup.find_all("span", class_="article-meta-value")[-1].text
    dateList = dateStr.split(' ')
    if len(dateList) == 5:
        year, month, day, time = dateList[4], dateList[1], dateList[2], dateList[3]
        month = __getMonth(month)
        time = time.split(':')
        hours, minutes, seconds = time 
        return f'{year}-{month}-{day} {hours}:{minutes}:{seconds}'

def __getMonth(month):
    if month == 'Jan':
        return '1'
    elif month == 'Feb':
        return '2'
    elif month == 'Mar':
        return '3'
    elif month == 'Apr':
        return '4'
    elif month == 'May':
        return '5'
    elif month == 'Jun':
        return '6'
    elif month == 'Jul':
        return '7'
    elif month == 'Aug':
        return '8'
    elif month == 'Sep':
        return '9'
    elif month == 'Oct':
        return '10'
    elif month == 'Nov':
        return '11'
    elif month == 'Dec':
        return '12'