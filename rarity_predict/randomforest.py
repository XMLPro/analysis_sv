import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

info = pd.read_pickle('../cards_info.pickle')

img_list = np.load('./img_arr.npy')
img_list = img_list[:, :, :, :3]
print(img_list.shape)
rarity = info[info.index=='rarity'].T

rarity[rarity['rarity'] == 'ブロンズレア'] = 0
rarity[rarity['rarity'] == 'シルバーレア'] = 1
rarity[rarity['rarity'] == 'ゴールドレア'] = 2
rarity[rarity['rarity'] == 'レジェンド'] = 3

# use a full grid over all parameters
param_grid = {"max_depth": [2,3, None],
             "n_estimators":[50,100,200,300,400,500],
             "max_features": [1, 3, 10],
             "min_samples_split": [2, 3, 10],
             "min_samples_leaf": [1, 3, 10],
             "bootstrap": [True, False],
             "criterion": ["gini", "entropy"]}

# clf = RandomForestClassifier().fit(img_list.reshape(3265, 1122384), rarity.values.T[0])

gs = GridSearchCV(RandomForestClassifier(verbose=1), param_grid, verbose=1, cv=5)
gs.fit(img_list.reshape(3265, 1122384), rarity.values.T[0])

print(gs.best_score_)

