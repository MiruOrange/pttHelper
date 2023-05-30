
def getPreviousPage(soup):
    url = 'https://www.ptt.cc'+soup.find('div', 'btn-group btn-group-paging').select('a')[1]['href']
    return url