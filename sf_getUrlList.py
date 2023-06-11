'''
兩個函式的目標是要取出不同來源資料的url

1. getUrlList, 是取出爬蟲後的url, 類型為list
2. getUrlFromTuppleInList, 是取出資料庫撈出的url, 類型為tupple
'''
def getUrlList(articleList):
    urlList = []
    for article in articleList:
        urlList.append(article['url'])
    return urlList

def getUrlFromTuppleInList(articleList):
    urlList = []
    for tuple in articleList:
        urlList.append(tuple[2])
    return urlList