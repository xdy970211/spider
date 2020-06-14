import requests
from contextlib import closing

download_header = {'Referer': 'https://www.dmzj.com/view/yaoshenji/41917.html'}
dn_url = 'https://images.dmzj.com/img/chapterpic/3059/14237/14395217739069.jpg'

with closing(requests.get(dn_url, headers = download_header, stream = True)) as response:
    chunk_size = 1024
    content_size = int(response.headers['content-length'])
    print(content_size)
    if response.status_code == 200:
        print('文件大小： %0.2f KB' % (content_size/chunk_size))
        with open('1.jpg', 'wb') as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
    else:
        print('链接异常')
print('下载完成！')

