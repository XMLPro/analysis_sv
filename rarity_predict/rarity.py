import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.utils import np_utils
import keras.applications.vgg16 as vgg16
from keras.optimizers import Adam
from keras.layers import Conv2D, MaxPooling2D, Flatten
import keras
from keras.utils import plot_model

from keras.preprocessing.image import load_img,img_to_array
from tqdm import tqdm

info = pd.read_pickle('../cards_info.pickle')

img_list = np.load('./img_arr.npy')
img_list = img_list[:, :, :, :3]
print(img_list.shape)
rarity = info[info.index=='rarity'].T

rarity[rarity['rarity'] == 'ブロンズレア'] = 0
rarity[rarity['rarity'] == 'シルバーレア'] = 1
rarity[rarity['rarity'] == 'ゴールドレア'] = 2
rarity[rarity['rarity'] == 'レジェンド'] = 3

y = np_utils.to_categorical(rarity.values)

# 先に作成したmodelへレイヤーを追加
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(4, activation='softmax'))

model.compile(loss='categorical_crossentropy',optimizer='Adam', metrics=['acc'])
          
print(img_list.shape)
print(y.shape)

# 学習処理の実行 -> 変数histに進捗の情報が格納される
hist = model.fit(img_list, y, batch_size=32, verbose=1, epochs=5, validation_split=0.1)
plot_model(model, to_file='rarity_predictor.png', show_shapes=True)

model.save('rarity_predictor2.h5')
