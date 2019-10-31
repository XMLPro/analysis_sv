import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tqdm import tqdm

info = pd.read_pickle('../cards_info.pickle')
img_list = []

for name in tqdm(info):
    img = plt.imread('../' + info[name]['path'])
    img_list.append(img)

img_list = np.array(img_list)
np.save('tmp.npy', img_list)

