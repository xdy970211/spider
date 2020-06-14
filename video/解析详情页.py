import requests
from bs4 import BeautifulSoup

detail_url = 'http://www.jisudhw.com/?m=vod-detail-id-15409.html'
r = requests.get(url = detail_url)
r.encoding = 'utf-8'
detail_bf = BeautifulSoup(r.text, 'lxml')
num = 1
search_res = {}
for each_url in detail_bf.find_all('input'):
    if 'm3u8' in each_url.get('value'):
        url = each_url.get('value')
        if url not in search_res.keys():
            search_res[url] = num
        print('第%03d集：' % num)
        print(url)
        num += 1