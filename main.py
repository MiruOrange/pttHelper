import requests
from bs4 import BeautifulSoup
import sf_getContentToDatabase as content
import sf_getPreviousPage as previous

url = 'https://www.ptt.cc/bbs/job/index.html'
cookies = {'over18':'1'}
for i in range(3):
    htmlFile = requests.get(url, cookies= cookies)
    soup = BeautifulSoup(htmlFile.text, 'lxml')
    content.getContent(soup)
    url = previous.getPreviousPage(soup)
