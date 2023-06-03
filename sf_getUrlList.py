
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