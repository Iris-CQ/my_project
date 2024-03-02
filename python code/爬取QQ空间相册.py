import os
import shutil
from urllib.request import urlretrieve

import requests
from selenium.common import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# 创建Chrome WebDriver对象
driver = webdriver.Chrome()

url='https://qzone.qq.com/'
# headers = {

# photo_path="D:/CQ相册/{}/{}.jpg"  #照片保存路径

driver.get(url)
element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "QZ_Toolbar_Container")))
menu=driver.find_element(By.XPATH,'//*[@class="head-nav-menu"]') #选择菜单：主页、日志、相册等
menu.find_element(By.CLASS_NAME,'menu_item_4').click()  #选择 相册
sleep(5)
driver.switch_to.frame(0)  #进入相册frame
attempts = 0
while attempts < 2:
    try:
        # element=driver.find_element(By.CLASS_NAME,'js-album-list-ul')
        # LIS=element.find_elements(By.TAG_NAME,'li')  #获取所有相册
        LIS = driver.find_elements(By.XPATH, '//*[@id="js-album-list-noraml"]/div/div/ul/li')  # 获取所有相册

        for i in range(7,len(LIS)):
            qq=LIS[i].find_element(By.CLASS_NAME,'album-tit').text
            if os.path.exists('D:/CQ相册/'+qq):
                shutil.rmtree('D:/CQ相册/'+qq)
            os.makedirs('D:/CQ相册/'+qq,True)
            LIS[i].find_element(By.CLASS_NAME,'album-cover').click() #点击打开相册album-cover js-album-cover
            sleep(3)
            driver.find_element(By.CLASS_NAME, 'item-cover').click() #点击第一张照片item-cover j-pl-photoitem-imgctn
            sleep(5)
            driver.switch_to.default_content()
            counts=driver.find_element(By.XPATH,'//*[@id="js-ctn-infoBar"]/div/div[1]/span').text
            counts=counts.split('/')
            for i in range(0,int(counts[1])):
                photos = driver.find_elements(By.XPATH, '//*[@id="js-thumbList-ctn"]/li')
                photos[i].find_element(By.TAG_NAME,'img').click()
                img = driver.find_element(By.ID, 'js-img-disp')
                # src=img.get_attribute('src').replace('&t=5','')
                src = img.get_attribute('src')
                name = driver.find_element(By.ID, 'js-photo-name').text
                r = requests.get(src)
                with open('D:/CQ相册/'+qq+'/'+name+'.jpg', 'wb') as f:
                    f.write(r.content)
                    f.close()
                    print(name+'保存成功')
                sleep(1)
            # sleep(2)

            # # urlretrieve(src,photo_path.format(qq,name))
            # counts=driver.find_element(By.XPATH,'//*[@id="js-ctn-infoBar"]/div/div[1]/span').text
            # counts=counts.split('/')
            # for item in range(0,int(counts[1])):
            # # while True:
            #     img = driver.find_element(By.ID, 'js-img-disp')
            #     # src=img.get_attribute('src').replace('&t=5','')
            #     src = img.get_attribute('src')
            #     name = driver.find_element(By.ID, 'js-photo-name').text
            #     r = requests.get(src)
            #     with open('D:/CQ相册/'+qq+'/'+name+'.jpg', 'wb') as f:
            #         f.write(r.content)
            #         f.close()
            #         print(name+'保存成功')
            #     sleep(1)
            #     if os.path.exists('D:/CQ相册/'+qq+'/'+name+'.jpg') and int(counts[0])<int(counts[1]):
            #         for i in (1,10):
            #             if driver.find_element(By.ID,'js-btn-nextPhoto'):
            #                 # driver.find_element(By.ID, 'js-btn-nextPhoto').click()
            #                 n=driver.find_element(By.ID, 'js-btn-nextPhoto')
            #                 ActionChains(driver).click(n).perform()
            #                 break
            #             else:
            #                 sleep(5)
            #     else:
            #         break

                # for i in (1,10):
                #     if driver.find_element(By.ID,'js-btn-nextPhoto'):
                #         driver.find_element(By.ID, 'js-btn-nextPhoto').click()
                #         # n=driver.find_element(By.ID, 'js-btn-nextPhoto')
                #         # ActionChains(driver).click(n).perform()
                #         break
                #     else:
                #         sleep(3)
            # sleep(2)
            # driver.find_element(By.XPATH,'//*[@id="js-recom-closeBtn"]').click() #点击查看更多
            sleep(2)
            driver.find_element(By.XPATH, '//*[@id="js-viewer-main"]/div[1]/a').click()  # 点击关闭大图
            sleep(1)
            driver.find_element(By.XPATH,'//*[@id="menuContainer"]/div/ul/li[3]/a').click()
            sleep(3)
            frame=driver.find_element(By.ID,'tphoto')
            driver.switch_to.frame(frame)
            sleep(1)
            # driver.switch_to.frame(0)  # 进入相册frame
            # driver.find_element(By.XPATH,'//*[@id="js-nav-container"]/div/div[1]/ul/li[1]/a').click()
            # element = driver.find_element(By.CLASS_NAME, 'js-album-list-ul')
            LIS = driver.find_elements(By.XPATH, '//*[@id="js-album-list-noraml"]/div/div/ul/li')  # 获取所有相册
            print(len(LIS))
            sleep(3)

        break
    except StaleElementReferenceException:
        attempts += 1

sleep(3600)
