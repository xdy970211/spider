import requests
from bs4 import BeautifulSoup


search_keyword = '越狱第一季'

search_url = 'http://www.jisudhw.com/index.php'
search_params = {
    'm': 'vod-search'
}

search_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    #'Referer': 'http://www.jisudhw.com/?m=vod-index-pg-2.html',
    'Referer': 'http://www.jisudhw.com/',
    'Origin': 'http://www.jisudhw.com',
    'Host': 'www.jisudhw.com'
}

search_datas = {
    'wd': search_keyword,
    'submit': 'search'
}

r = requests.post(url=search_url, params = search_params, headers = search_headers, data=search_datas)

r.encoding = 'utf-8'
server = 'http://www.jisudhw.com'
search_html = BeautifulSoup(r.text, 'lxml')
search_spans = search_html.find_all('span', class_='xing_vb4')
for span in search_spans:
    url = server + span.a.get('href')
    name = span.a.string
    print(name)
    print(url)


