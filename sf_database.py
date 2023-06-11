import sqlite3
import sf_getUrlList as getUrl

#連結資料庫，如果沒有該資料庫，則會建立一個新的
def connectTodb(filePath):
    return sqlite3.connect(filePath)

#建立table
def createDbTables(db, tableName):
        sql = f'''
        CREATE TABLE IF NOT EXISTS {tableName} (
            author TEXT, 
            title TEXT,
            url TEXT,
            push INTEGER,
            createDate DATE,
            articleContent TEXT,
            articleDiscuss TEXT
        )
        '''
        db.execute(sql)
        print(tableName, '表單建立完成')

# 1.從該表單篩選出全部的資料(未來資料多了以後, 可以加上篩選的區間)
# 2.比對該次爬蟲爬到的資料, 是否已經存在資料庫中
    # 如果不存在, 則直接存入
    # 如果存在, 則更新push數
    # 判斷資料是否已存在資料庫中, 以該筆文章的url為比對條件, 因為文章的url具有唯一性
def saveData(db, tableName, articleList):
    # 取出db所有資料
    selectSql = "SELECT * FROM {}"                               # 括號中準備放入各表單名稱
    sql = selectSql.format(tableName)                            # 取出表單名稱name放入
    dbData = db.execute(sql).fetchall()                          # 從db中取出現有url

    
    dbUrlList = getUrl.getUrlFromTuppleInList(dbData)           # 單獨取出db所有的url
    urlList = getUrl.getUrlList(articleList)                    # 取出該次爬蟲資料的url
    
    urlNotExistYet = [x for x in urlList if x not in dbUrlList]  # 該次爬蟲資料url不存在db的清單  
    urlExists = [x for x in urlList if x in dbUrlList]           # 該次爬蟲資料url已存在db的清單
    
    
    #db 處理
    for article in articleList:
        #如果url存在 urlNotExistYet, 則存入db
        if article['url'] in urlNotExistYet:
            addSql = "INSERT INTO {} (author, title, url, push, createDate, articleContent, articleDiscuss) VALUES (?, ?, ?, ?, ?, ?, ?)"
            values = (article['author'], article['title'], article['url'], article['push'], article['pushDate'], article['articleContent'], article['articleDiscuss'])
            db.execute(addSql.format(tableName), values)
            db.commit()
        #如果url存在 urlExists, 則更新push
        if article['url'] in urlExists:
            updateSql = "UPDATE {} SET push = ?, title = ?, articleContent = ?, articleDiscuss = ? WHERE url = ?"
            values = (article['push'], article['title'], article['url'], article['articleContent'], article['articleDiscuss'])    #更新title, 是有時user會更新文章標題
            db.execute(updateSql.format(tableName), values)
            db.commit()