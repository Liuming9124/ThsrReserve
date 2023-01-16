import cv2
import numpy as np
from PIL import Image
# from sklearn.preprocessing import binarize
# import matplotlib.pyplot as plt

def preprocessed():
    filename = './cap_login.jpg'
    # clear RGBA to RGB
    # im = Image.open('./cap_login.png')
    # # im.show()
    # rgb_im = im.convert('RGB')
    # while(1):
    #     if (rgb_im.save(filename)):
    #         continue
    #     else:
    #         break

    # -------------resize----------
    img = Image.open(filename)
    # img.show()
    newimg = img.resize((140, 48))
    # newimg.show()
    while(1):
        if (newimg.save(filename)):
            continue
        else:
            break

    WIDTH = 140
    HEIGHT = 48

    img = cv2.imread( filename)

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

    cv2.imwrite('./' + filename, newimg)

    pred_ds=[]
    # 先長後寬 先左上角後右下角
    split0 = ( 20, 0, 45,48)
    split1 = ( 45, 0, 70,48)
    split2 = ( 70, 0, 95,48)
    split3 = ( 95, 0,120,48)

    path = filename
    img = cv2.imread(path)
    pred_ds.append(img[split0[1]:split0[3], split0[0]: split0[2]])
    pred_ds.append(img[split1[1]:split1[3], split1[0]: split1[2]])
    pred_ds.append(img[split2[1]:split2[3], split2[0]: split2[2]])
    pred_ds.append(img[split3[1]:split3[3], split3[0]: split3[2]])

    return pred_ds
# preprocessed()