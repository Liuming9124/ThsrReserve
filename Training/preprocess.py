# 將驗證碼預處理


import cv2
import numpy as np
from PIL import Image
# from sklearn.preprocessing import binarize
import matplotlib.pyplot as plt


# -------------resize----------
# for i in range(10000,10101):
#     filename = './captcha/'+str(i)+'.jpg'
#     img = Image.open(filename)
#     # img.show()
#     newimg = img.resize((140, 48))
#     # newimg.show()
#     while(1):
#         if (newimg.save(filename)):
#             continue
#         else:
#             break
#     print(i)
# input()


WIDTH = 140
HEIGHT = 48

CAPTCHA_FOLDER = "captcha/"
PROCESSED_FOLDER = "processed/"

for i in range(10001,10101):
    print(i)
    filename = str(i) + '.jpg'
    img = cv2.imread(CAPTCHA_FOLDER + filename)

    dst = cv2.fastNlMeansDenoisingColored(img, None, 30, 30, 7, 21)
    # plt.subplot(121)
    # plt.imshow(img)
    # plt.subplot(122)
    # plt.imshow(dst)
    # plt.show()

    ret, thresh = cv2.threshold(dst, 127, 255, cv2.THRESH_BINARY_INV)
    # plt.imshow(thresh)
    # plt.show()

    imgarr = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    imgarr[:, 14:WIDTH - 7] = 0
    imagedata = np.where(imgarr == 255)

    imgarr.shape

    X = np.array([imagedata[1]])
    Y = HEIGHT - imagedata[0]

    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.linear_model import LinearRegression

    poly_reg = PolynomialFeatures(degree = 2)
    X_ = poly_reg.fit_transform(X.T)
    regr = LinearRegression()
    regr.fit(X_, Y)


    X2 = np.array([[i for i in range(0, WIDTH)]])

    X2_ = poly_reg.fit_transform(X2.T)


    # plt.scatter(X, Y, color = "black")
    # plt.ylim(ymin = 0)
    # plt.ylim(ymax = HEIGHT)
    # plt.plot(X2.T, regr.predict(X2_), color = "blue", linewidth = 18)

    newimg = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    offset = 4
    for ele in np.column_stack([regr.predict(X2_).round(2), X2[0]]):
        pos = HEIGHT - int(ele[0])
        newimg[pos - offset:pos + offset, int(ele[1])] = 255 - newimg[pos - offset:pos + offset, int(ele[1])]

    # plt.imshow(newimg)
    # plt.show()


    cv2.imwrite(PROCESSED_FOLDER + filename, newimg)