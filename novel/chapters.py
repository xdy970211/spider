import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    server = 'https://www.xsbiquge.com'
    target = 'https://www.xsbiquge.com/15_15338/'
    req = requests.get(url = target)
    req.encoding = 'utf-8'
    html = req.text
    bs = BeautifulSoup(html, 'lxml')
    content = bs.find('div', id = 'list')
    content = content.find_all('a')
    for chapter in content:
        url = chapter.get('href')
        print(chapter.string)
        print(server + url)