'''
解析取得的soup檔
'''
import sf_pushCalculator as push
import requests
from bs4 import BeautifulSoup

def getContent(soup, tableName):
    articleData = soup.select('.r-ent')
    articles = []
    for article in articleData:
        if article.find('a') !=None:        #文章被刪除時，標題會變None，所以要加此判斷式
            title = article.find('a').text
            if '公告' in title:              #公告的文章, 一來不需要, 二來常有不預期的格式出現
                continue
            else:
                url = article.find('a')['href']
                url = 'https://www.ptt.cc'+url
                author = article.find('div', 'author').text
                pushAmount = article.find('div', 'nrec').text
                pushAmount = push.pushCalculator(pushAmount)    #回傳為int
                pushDate = __getPushDate(url)                   #取得發文日期
                if tableName == 'gossip':
                    articleContent, articleDiscuss = __getContentAndDiscuss(url)    #取得內文及推噓文內容
                    if pushDate == 'No Data':             # 有遇到發文的格式很奇怪, 應該是刪掉了標頭的部份, 造成程式錯誤, 故增加此行
                        continue
                    else:
                        articles.append({                  #self.articles陣列存放字典資料
                            'author':author,
                            'title':title, 
                            'push':pushAmount,  #pushAmount為int
                            'pushDate':pushDate,
                            'url' : url,
                            'articleContent':articleContent,
                            'articleDiscuss':articleDiscuss
                        })
                else:
                    if pushDate == 'No Data':             # 有遇到發文的格式很奇怪, 應該是刪掉了標頭的部份, 造成程式錯誤, 故增加此行
                        continue
                    else:
                        articles.append({                  #self.articles陣列存放字典資料
                            'author':author,
                            'title':title, 
                            'push':pushAmount,  #pushAmount為int
                            'pushDate':pushDate,
                            'url' : url,
                            'articleContent':'不是八掛版, 不用存',
                            'articleDiscuss':'不是八掛版, 不用存'
                        })

    return articles
    #準備在此存入db

# 取得發文日期, 轉成%Y-%m-%d %H:%M:%S格式, 準備存入db
def __getPushDate(url):
    cookies = {'over18':'1'}
    htmlFile = requests.get(url, cookies= cookies)  #帶入cookie, 直接跳過18歲的選單
    soup = BeautifulSoup(htmlFile.text, 'lxml')
    if soup.find_all("span", class_="article-meta-value") != []:
        dateStr = soup.find_all("span", class_="article-meta-value")[-1].text
        dateList = dateStr.split(' ')
        if len(dateList) == 5:
            year, month, day, time = dateList[4], dateList[1], dateList[2], dateList[3]
            month = __getMonth(month)
            time = time.split(':')
            hours, minutes, seconds = time 
            return f'{year}-{month}-{day} {hours}:{minutes}:{seconds}'
        #[thu, jun, , 1, 22:57:10, 2023]
        elif len(dateList) == 6:
            year, month, day, time = dateList[5], dateList[1], dateList[3], dateList[4]
            month = __getMonth(month)
            time = time.split(':')
            hours, minutes, seconds = time
            return f'{year}-{month}-{day} {hours}:{minutes}:{seconds}'
    else:
        return 'No Data'
    
def __getMonth(month):
    dayDict = {
        'Jan':'1', 'Feb':'2', 'Mar':'3', 'Apr':'4', 'May':'5', 'Jun':'6',
        'Jul':'7', 'Aug':'8', 'Sep':'9', 'Oct':'10', 'Nov':'11', 'Dec':'12'
    }
    return dayDict[month]

def __getContentAndDiscuss(url):
    cookies = {'over18':'1'}
    htmlFile = requests.get(url, cookies= cookies)  #帶入cookie, 直接跳過18歲的選單
    soup = BeautifulSoup(htmlFile.text, 'lxml')
    fullContent = soup.find('div', id='main-content').get_text()
    if '※ 發信站: 批踢踢實業坊(ptt.cc)' in fullContent:
        articleContent = fullContent.split('※ 發信站: 批踢踢實業坊(ptt.cc)')[0]
        articleDiscuss = fullContent.split('※ 發信站: 批踢踢實業坊(ptt.cc)')[1].split('.html')[1] 
        return articleContent, articleDiscuss
    else:
        print(fullContent)
        print(url)
        return '文章格式錯誤, 出錯的url='+url, '文章格式錯誤, 出錯的url='+url   #回傳兩個變數才不會出錯