import requests
import bs4
from tqdm import tqdm
import time
import pandas as pd
import re


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

def get_card_info(path='./img/'):
    # 何ページ目かを示す。
    count = 0
    url = 'https://shadowverse-portal.com/cards?m=index&lang=ja&m=index&card_offset='
    # pack, skillには現状何も入らない
    info = pd.DataFrame(index=['path', 'type', 'class', 'rarity', 'cv', 'pack', 'skill'])

    while True:
        # 1page 12枚なので
        try:
            source = requests.get(url + str(count * 12)).text
        except:
            print('error')
            time.sleep(10)
            source = requests.get(url + str(count * 12)).text

        soup = bs4.BeautifulSoup(source, 'html.parser')
        cards = soup.select(".el-card-visual-content")
        if not cards:
            break

        for card in tqdm(cards):
            card_url = f'https://shadowverse-portal.com/{card["href"]}?lang=ja'
            try:
                card_html = requests.get(card_url).text
            except:
                print('error')
                time.sleep(10)
                card_html = requests.get(card_url).text

            card_soup = bs4.BeautifulSoup(card_html, 'html.parser')

            name = card_soup.select_one('.card-main-title').text
            name = name.replace('\n', '')
            name = name.replace('\r', '')
            info[name] = 'None'

            card_info_soup = card_soup.select('.card-info-content span')
            for num, card_info in enumerate(card_info_soup):
                card_info = card_info.text
                card_info = card_info.replace('\n', '')
                card_info = card_info.replace('\r', '')

                # 最悪だけどこうするしかなさそう
                # 実際ここのせいで、うまく取れない情報が多い
                if num == 1:
                    info[name]['type'] = card_info
                if num == 3:
                    info[name]['class'] = card_info
                if num == 5:
                    info[name]['rarity'] = card_info
                if num == 12:
                    info[name]['cv'] = card_info
                if num == 14:
                    info[name]['pack'] = card_info

            info[name]['path'] = path + 'normal/' + name + '.png'
            img_list = card_soup.select('.card-main-image')
            for i, img in enumerate(img_list):
                img = img.select('img')
                # カードの画像の上に名前の画像を載せるという方法を取っているので、
                # 1つ飛ばして名前の画像は取らないようにしてる。
                for img_url in img[::2]:
                    img_url = img_url['src']
                    if i == 1:
                        info[f'evo_{name}'] = info[name]
                        name = f'evo_{name}'
                        info[name]['path'] = path + 'evo/' + name + '.png'
                    with open(info[name]['path'], 'wb') as f:
                        try:
                            img_content = requests.get(img_url).content
                        except:
                            print('error')
                            time.sleep(10)
                            card_html = requests.get(card_url).text
                        f.write(img_content)

                    time.sleep(1)

        count += 1

    print('finished!!')
    return info



if __name__ == '__main__':
    info = get_card_info()
    info.to_pickle('./cards_info.pickle')
    print(info)
