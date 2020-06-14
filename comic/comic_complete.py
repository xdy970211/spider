import requests
import os
import re
from bs4 import BeautifulSoup
from contextlib import closing
from tqdm import tqdm
import time

save_dir = '妖神记'
if save_dir not in os.listdir('../'):
    os.mkdir(save_dir)

target_url = 'https://www.dmzj.com/info/yaoshenji.html'
req = requests.get(url = target_url)
#req.encoding = 'utf-8'
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

for i, url in enumerate(tqdm(chapter_urls)):
    download_header = {'Referer': url}
    name = chapter_names[i]
    while '.' in name:
        name = name.replace('.', '')
    chapter_save_dir = os.path.join(save_dir, name)
    if name not in os.listdir(save_dir):
        os.mkdir(chapter_save_dir)
        r = requests.get(url = url)
        #print('success')
        html = BeautifulSoup(r.text, 'lxml')
        script_info = str(html.script)
        pics = re.findall('\d{13,14}', script_info)

        for idx, pic in enumerate(pics):
            if len(pic) == 13:
                pics[idx] = pic + '0'
        #print('success1')
        pics = sorted(pics, key = lambda x: int(x))
        chapterpic_hou = re.findall('\|(\d{5})\|', script_info)[0]
        chapterpic_qian = re.findall('\|(\d{4})\|', script_info)[0]

        for idx, pic in enumerate(pics):
            if pic[-1] == '0':
                url = 'https://images.dmzj.com/img/chapterpic/' + chapterpic_qian + '/'\
                      + chapterpic_hou + '/' + pic[:-1] + '.jpg'
            else:
                url = 'https://images.dmzj.com/img/chapterpic/' + chapterpic_qian + '/'\
                      + chapterpic_hou + '/' + pic + '.jpg'

            pic_name = '%03d.jpg' % (idx + 1)
            pic_save_path = os.path.join(chapter_save_dir, pic_name)
            with closing(requests.get(url, headers = download_header, stream = True)) as response:
                chunk_size = 1024
                content_size = int(response.headers['content-length'])
                if response.status_code == 200:
                    with open(pic_save_path, 'wb') as file:
                        for data in response.iter_content(chunk_size=chunk_size):
                            file.write(data)
                else:
                    print('链接异常')
        time.sleep(5)
