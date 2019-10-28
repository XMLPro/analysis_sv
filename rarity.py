import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np
import keras
from keras.preprocessing.image import load_img,img_to_array
from tqdm import tqdm

info = pd.read_pickle('./cards_info.pickle')

img_list = []

#ファイルパスのリストをもとに画像を配列化
for card_info in tqdm(info):
    img = plt.imread(info[card_info]['path'])
    img_list.append(img)

print(img_list)
