from keras.models import load_model
import numpy as np
from preprocessed import preprocessed


def decode (de):
    output=[]
    allow_chars = ['H', 'R', '3', '7', '5', 'Y', 'F', 'Z', 'C', '9', 'Q', 'T', 'N', '2', 'P', 'A', 'K', 'M', '4', '6', 'V', 'D', 'W', 'G']
    for i in range(4):
        j = de[i]
        output.append(allow_chars[j])
    return output

def predicts (inputs,model):
    de = np.argmax(model.predict(inputs[0:4]),axis=1)
    return decode(de)



def get_cap():
    model = load_model('model.h5',compile=False)
    inputs = np.array(preprocessed())
    # print('getinput= ',inputs)
    decode = predicts(inputs,model)
    return decode

if __name__=='__main__':
    # 載入模型
    model = load_model('model.h5',compile=False)
    print(get_cap())