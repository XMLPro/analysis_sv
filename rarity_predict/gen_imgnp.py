from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tqdm import tqdm

info = pd.read_pickle('../cards_info.pickle')
def read_card():
    img_list = []

    for name in tqdm(info):
        img = plt.imread('../' + info[name]['path'])
        img_list.append(img)

    img_list = np.array(img_list)
    return img_list


def resize(img_list=np.load('./img_arr.npy'):
    img_list = img_list[:, :, :, :3]
    img_list2 = []

    for img in tqdm(img_list):
        img = Image.fromarray(np.uint8(img))
        resize_img = np.asarray(img.resize((img_list.shape[1] // 4, img_list.shape[2] // 4)))
        img_list2.append(resize_img)

    img_list2 = np.array(img_list2)
    np.save('small_card.npy', img_list2)

resize()
