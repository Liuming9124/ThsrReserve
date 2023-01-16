from multiprocessing.connection import wait
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import base64

# 等待開始時間 幾點開始搶
time = '12/21/22 00:00:00'
endTime = datetime.strptime(time, '%m/%d/%y %H:%M:%S')



# wait
while True:
  if datetime.now() >= endTime:
    break



# 檢查元素是否存在
def check_element_exists(driver, element, condition):
    try:
        # if condition == 'class':
        #     driver.find_element(By.CLASS,(element))
        if condition == 'ID':
            driver.find_element(By.ID,(element))
        elif condition == 'XPATH':
            driver.find_element(By.XPATH,(element))
        return True
    except Exception as e:
        return False




while(1):
  delay = 0.1
  url = "https://irs.thsrc.com.tw/IMINT/"
  # chrome = webdriver.Chrome("D:\Desktop\THSR\chromedriver.exe")
  option = webdriver.ChromeOptions()
  option.add_experimental_option('excludeSwitches', ['enable-automation'])
  chrome = webdriver.Chrome(options=option,executable_path='.\chromedriver')
  chrome.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
      Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
      })
    """
  })

  chrome.get(url)
  # print(chrome.page_source)
  sleep(delay)

  #cookie agreement button
  agree = chrome.find_element(By.ID, "cookieAccpetBtn")
  agree.click()


  # while直到輸入成功
  while (1):

    #select start station
    start = Select(chrome.find_element(By.NAME, "selectStartStation"))
    start.select_by_visible_text("台北")
    #select end station
    end   = Select(chrome.find_element(By.NAME, "selectDestinationStation"))
    end.select_by_visible_text("板橋")
    #select time
    stime = Select(chrome.find_element(By.NAME, "toTimeTable"))
    stime.select_by_visible_text("16:00")
    #select 全票
    adult = Select(chrome.find_element(By.NAME, "ticketPanel:rows:0:ticketAmount"))
    adult.select_by_visible_text('0')
    #select 大學生票
    univer = Select(chrome.find_element(By.NAME, "ticketPanel:rows:4:ticketAmount"))
    univer.select_by_visible_text('1')
    #choose day
    date = "2023/02/5"
    js = 'document.getElementById("toTimeInputField").value = "' + str(date) +'"'
    chrome.execute_script(js)


    #驗證碼

    img = chrome.find_element(By.XPATH, '//*[@id="BookingS1Form_homeCaptcha_passCode"]')
    img= img.screenshot_as_base64
    with open("./cap_login.png", 'wb') as image:
        # image.write(img)
        image.write(base64.b64decode(img))


    from PIL import Image
    # clear RGBA to RGB
    im = Image.open('./cap_login.png')
    # im.show()
    rgb_im = im.convert('RGB')
    rgb_im.save('./cap_login.jpg')


    # get cap_login
    from predict import get_cap
    cap = get_cap()
    cap_login = f'{cap[0]}{cap[1]}{cap[2]}{cap[3]}'
    print(cap_login)


    #put cap in input box
    # chrome.find_element(By.XPATH,'//*[@id="securityCode"]').submit(cap_login)
    chrome.execute_script(f"document.getElementById('securityCode').value=('{cap_login}')")


    # sleep(10)
    #start search
    search = chrome.find_element(By.ID, "SubmitButton").click()
    if(check_element_exists(chrome,'//*[@id="BookingS1Form_homeCaptcha_passCode"]','XPATH')):
      continue
    else:
      break

  #第一次輸入可能會卡在請稍後 -> 請稍後資訊: id = 'loadingMask' => 尚未處理
  
  sleep(delay)
  while(1):
    if(check_element_exists(chrome,'//*[@id="BookingS2Form"]/section[2]/div/div/input','XPATH')):
      chrome.find_element(By.XPATH,'//*[@id="BookingS2Form"]/section[2]/div/div/input').click()
      break
  
  # 判斷已進入輸入個人資訊
  while(1):
    if(check_element_exists(chrome,'//*[@id="BookingS3FormSP"]/section[2]/div[1]','XPATH')):
      break
  # 輸入個人資料 身分證字號 電話 Email
  pid = 'A12345678'
  pphone = '0912345678'
  pemail = '123@gmail.com'

  chrome.execute_script(f"document.getElementById('idNumber').value=('{pid}')")
  chrome.execute_script(f"document.getElementById('mobilePhone').value=('{pphone}')")
  chrome.execute_script(f"document.getElementById('email').value=('{pemail}')")

  #是否有會員 有->取消註解
  # chrome.find_element(By.ID,('memberSystemRadio1')).click()
  # chrome.find_element(By.ID,('memberShipCheckBox')).click()
  
  #將我已明確了解打勾
  chrome.find_element(By.XPATH,('//*[@id="BookingS3FormSP"]/section[2]/div[3]/div[1]/label/input')).click()
  
  #完成訂位
  chrome.find_element(By.ID,('isSubmit')).click()
  
  #最後確認
  sleep(10)
  if(check_element_exists(chrome,'btn-custom2','ID')):
    chrome.find_element(By.ID,('btn-custom2')).click()  


  sleep(10)
  chrome.close()
