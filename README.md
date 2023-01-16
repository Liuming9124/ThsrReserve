# ThsrReserve
# Use Tensorflow, CNN, Keras Create Model
# 建立高鐵搶票系統
# Reserving
* model.h5 -> 訓練好的model
* predict.py -> 取得驗證碼且decode後回傳
* prepossed.py -> 將驗證碼預處理後回傳分割成四個digit的array
* thsr.py -> 主程式:自動搶票
# Training
* ## cap : 存放驗證碼
* ## prepossed : 存放預處理後的驗證碼
* label.csv -> 存放驗證碼string
* predict.ipynb -> 驗證預測
* repeat.py -> 回傳沒有重複的字元 (小工具)
* train.py -> 處理資料並訓練模型
* buildmodel.py -> 建立模型
 ![image](https://user-images.githubusercontent.com/80050536/212624170-7e310fb3-4023-41ee-a4b7-904653cbd677.png)
