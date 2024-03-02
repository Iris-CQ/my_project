from selenium.common import StaleElementReferenceException
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


driver.get(url)
element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "QZ_Toolbar_Container")))
menu=driver.find_element(By.XPATH,'//*[@class="head-nav-menu"]')
menu.find_element(By.CLASS_NAME,'menu_item_2').click()
sleep(5)
driver.switch_to.frame(0)
attempts = 0
while attempts < 2:
    try:
        element=driver.find_element(By.ID,'listArea')
        LIS=element.find_elements(By.TAG_NAME,'li')
        LIS[0].find_element(By.TAG_NAME,'a').click()
        # driver.find_element(By.XPATH,'//*[@id="listArea"]/div/ul/li[1]/div/div[1]/h4/a').click()
        sleep(3)
        driver.switch_to.default_content()
        iframe_1 = driver.find_element(By.ID, 'tblog')
        driver.switch_to.frame(iframe_1)
        for i in range(1, 100):
            nrs = driver.find_elements(By.XPATH, '//*[@id="blogDetailDiv"]')
            # nrs = driver.find_elements(By.XPATH, '//*[@id="blogDetailDiv"]/div/div')
            title = driver.find_element(By.XPATH, '//*[@id="title"]/strong/span/span').text
            edit = driver.find_element(By.XPATH,'//*[@id="title"]/span').text
            commentCnt = driver.find_element(By.ID, 'commentCnt').text
            commentDivs = driver.find_elements(By.XPATH, '//*[@id="commentListDiv"]/li')
            with open(title + '.txt', 'w', encoding='utf-8') as file:
                text = title
                file.write(text + '\n')
                text = edit
                file.write(text + '\n')
                for nr in nrs:
                    text = nr.text
                    # sleep(2)
                    print(text)
                    file.write(text + '\n\n')
                text = commentCnt
                file.write(text + '\n')
                for comment in commentDivs:
                    username = comment.find_element(By.CLASS_NAME,'username').text
                    text = username
                    file.write(text + " ")
                    comment_time = comment.find_element(By.XPATH,'//*[@class="c_tx3 time"]').text
                    text = comment_time
                    file.write(text+ '\n')
                    comment_DIT = comment.find_element(By.TAG_NAME, 'table').text
                    text = comment_DIT
                    file.write(text + '\n')
                    mod_comment = comment.find_element(By.CLASS_NAME, 'comments_list').text
                    text = mod_comment
                    file.write(text + '\n\n')


            sleep(3)
            NEXT = driver.find_element(By.ID, 'navigatorSpan1')
            NEXT.click()
            sleep(5)
            # element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'blogDetailDiv')))
        break
    except StaleElementReferenceException:
        attempts += 1




sleep(3600)

# driver.quit()