import requests
import time
from tqdm import tqdm
from bs4 import BeautifulSoup

def get_content(target):
    req = requests.get(url=target)
    req.encoding = 'utf-8'
    html = req.text
    bs = BeautifulSoup(html, 'lxml')
    texts = bs.find('div', id='content')
    content = texts.text.strip().split('\xa0' * 4)
    return content

if __name__ == '__main__':
    server = 'https://www.xsbiquge.com'
    book_name = '诡秘之主.txt'
    target = 'https://www.xsbiquge.com/15_15338/'
    req = requests.get(url=target)
    req.encoding = 'utf-8'
    html = req.text
    bs = BeautifulSoup(html, 'lxml')
    content = bs.find('div', id='list')
    chapters = content.find_all('a')
    for chapter in tqdm(chapters):
        url = server + chapter.get('href')
        chapter_name = chapter.string
        content = get_content(url)
        with open(book_name, 'a', encoding='utf-8') as f:
            f.write(chapter_name)
            f.write('\n')
            f.write('\n'.join(content))
            f.write('\n')