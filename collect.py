import requests
import bs4
from tqdm import tqdm
import time


def get_image():
    count = 0
    while True:
        url = 'https://shadowverse-portal.com/cards?m=index&lang=ja&m=index&card_offset='
        source = requests.get(url + str(count * 12)).text

        soup = bs4.BeautifulSoup(source, 'html.parser')
        res = soup.select(".el-card-frame-wrapper .el-card-visual-image")
        if not res:
            break

        for i in tqdm(res):
            img_src = i['data-src']
            img = requests.get(img_src).content
            with open('img/'+i['alt']+'.png', 'wb') as f:
                f.write(img)
        count += 1
        time.sleep(1)


    print('finished collecting img')

if __name__ == '__main__':
    get_image()

