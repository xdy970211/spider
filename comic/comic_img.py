import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.dmzj.com/view/yaoshenji/41917.html'
r = requests.get(url = url)
html = BeautifulSoup(r.text, 'lxml')
script_info = str(html.script)
pics = re.findall('\d{13,14}', script_info)

for idx, pic in enumerate(pics):
    if len(pic) == 13:
        pics[idx] = pic + '0'

pics = sorted(pics, key = lambda x: int(x))
chapterpic_hou = re.findall('\|(\d{5})\|', script_info)[0]
chapterpic_qian = re.findall('\|(\d{4})\|', script_info)[0]

for pic in pics:
    if pic[-1] == '0':
        url = 'https://images.dmzj.com.img/chapterpic/' + chapterpic_qian + '/'\
              + chapterpic_hou + '/' + pic[:-1] + '.jpg'
    else:
        url = 'https://images.dmzj.com.img/chapterpic/' + chapterpic_qian + '/'\
              + chapterpic_hou + '/' + pic + '.jpg'
    print(url)