import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from keras.models import load_model

def read_img(fname):
    img = plt.imread(fname)[:, :, :3]
    h = img.shape[0]
    w = img.shape[1]

    img = Image.fromarray(np.uint8(img))
    resize_img = np.asarray(img.resize((w // 4, h // 4)))
    img = np.asarray(img)

    return resize_img

if __name__ == '__main__':
    model = load_model('./rarity_predictor.h5')
    img = read_img('../img/evo/evo_神龍.png')
    print(model.summary())
    res = model.predict(np.array([img]))

    print(res)
