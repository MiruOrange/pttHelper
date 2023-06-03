import sqlite3
import sf_getUrlList as getUrl

#連結資料庫，如果沒有該資料庫，則會建立一個新的

def connectTodb(filePath):
    return sqlite3.connect(filePath)

def createDbTables(db, tableName):
        sql = f'''
        CREATE TABLE IF NOT EXISTS {tableName} (
            author TEXT, 
            title TEXT,
            url TEXT,
            push INTEGER,
            createDate DATE
        )
        '''
        db.execute(sql)
        print(tableName, '建立完成')

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

    # 單獨取出db所有的url
    dbUrlList = getUrl.getUrlFromTuppleInList(dbData)
    # 取出該次爬蟲資料的url
    urlList = getUrl.getUrlList(articleList)                     # 從爬下來的文章中, 取出url準備和db的資料做比對
    # 該次爬蟲資料url不存在db的清單
    urlNotExistYet = [x for x in urlList if x not in dbUrlList]  # 找出url不存在db的文章, 不存在, 則存入
    # 該次爬蟲資料url已存在db的清單
    urlExists = [x for x in urlList if x in dbUrlList]           # 找出url已存在db的文章, 已存在, 則更新push數
    
    
    #db 處理
    for article in articleList:
        #如果url存在 urlNotExistYet, 則存入db
        if article['url'] in urlNotExistYet:
            addSql = "INSERT INTO {} (author, title, url, push, createDate) VALUES (?, ?, ?, ?, ?)"
            values = (article['author'], article['title'], article['url'], article['push'], article['pushDate'])
            db.execute(addSql.format(tableName), values)
            db.commit()
        #如果url存在 urlExists, 則更新push
        if article['url'] in urlExists:
            updateSql = "UPDATE {} SET push = ? WHERE url = ?"
            values = (article['push'], article['url'])
            db.execute(updateSql.format(tableName), values)
            db.commit()