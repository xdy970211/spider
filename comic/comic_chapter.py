import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    target = 'https://www.dmzj.com/info/yaoshenji.html'
    req = requests.get(url = target)
    req.encoding = 'utf-8'
    html = req.text
    bs = BeautifulSoup(html, 'lxml')
    chapters = bs.find('ul', class_ = 'list_con_li')
    chapters = chapters.find_all('a')
    chapter_urls = []
    chapter_names = []
    for chapter in chapters:
        chapter_urls.append(chapter.get('href'))
        chapter_names.append(chapter.text)

    chapter_names.reverse()
    chapter_urls.reverse()
    print(chapter_names[:10])
    print(chapter_urls[:10])