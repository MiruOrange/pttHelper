from datetime import datetime
import sf_pushCalculator as push

def getContent(soup):
    articleData = soup.select('.r-ent')
    articles = []
    for article in articleData:
        if article.find('a') !=None:        #文章被刪除時，標題會變None，所以要加此判斷式
            title = article.find('a').text
            url = article.find('a')['href']
            author = article.find('div', 'author').text
            pushAmount = article.find('div', 'nrec').text
            pushAmount = push.pushCalculator(pushAmount)    #回傳為int
            issueDateList = article.find('div', 'date').text.strip().split('/')
            issueMonth = issueDateList[0]
            issueDay = issueDateList[1]
            issueYear = str(datetime.now().year)
            articles.append({                  #self.articles陣列存放字典資料
                'author':author,
                'title':title, 
                'push':pushAmount,  #pushAmount為int
                'year':issueYear,
                'month':issueMonth,
                'day':issueDay,
                'url' :'https://www.ptt.cc'+url
        })
    print(articles)
    #在此存入db