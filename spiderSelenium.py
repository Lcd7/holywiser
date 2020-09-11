from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from retry import retry
import os
from htmlClass import File


startPage = 1
Flag = True

def login(dr):
    dr.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div/div/header[1]/div/div/ul/div[2]/li[1]/button/span').click()
    time.sleep(1)
    dr.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/form/div[1]/div/div[1]/input').send_keys('')
    dr.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/form/div[2]/div/div/input').send_keys('')
    dr.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/div[3]/div/button[2]/span').click()
    time.sleep(1)


def pageTurn(dr, num):
    dr.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div/div/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div[1]/div[3]/div/ul/div/div/input').send_keys(Keys.CONTROL, 'a')
    dr.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div/div/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div[1]/div[3]/div/ul/div/div/input').send_keys(Keys.BACK_SPACE)
    dr.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div/div/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div[1]/div[3]/div/ul/div/div/input').send_keys(num)
    dr.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div/div/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div[1]/div[3]/div/ul/div/div/input').send_keys(Keys.ENTER)


def click_locxy(dr, x, y, left_click = True):
    '''
    dr:浏览器
    x:页面x坐标
    y:页面y坐标
    left_click:True为鼠标左键点击，否则为右键点击
    '''
    if left_click:
        ActionChains(dr).move_by_offset(x, y).click().perform()
    else:
        ActionChains(dr).move_by_offset(x, y).context_click().perform()
    ActionChains(dr).move_by_offset(-x, -y).perform() #  将鼠标位置恢复到移动前


@retry()
def run():
    global Flag
    global startPage

    url = "http://www.holywiser.com/search?classid="

    dr = webdriver.Chrome()
    dr.maximize_window()
    dr.get(url)
    dr.implicitly_wait(10)
    # actions = ActionChains(dr)

    # 进入主页
    dr.find_element_by_class_name("my-Btn").click()
    dr.implicitly_wait(10)

    # 登录
    login(dr)

    for num in range(startPage, 10):
        # 选择页数
        pageTurn(dr, num)

        # 获取文章
        num_file = 1
        time.sleep(3)

        # 循环进入一页的文章
        for _ in range(10):
            File.clear()

            # 文件名
            chaps = dr.find_elements_by_xpath('//*[@id="app"]/div/div/div[1]/div/div/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/table/tbody//a')
            chap = chaps[num_file-1]
            File.fileName = chap.text
            # 文号
            File.fileNum = dr.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div/div/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/table/tbody/tr[{}]/td[2]/div/span'.format(num_file)).text
            if File.fileNum == '':
                File.fileNum = '无'
    
            # 进入文章
            dr.execute_script("arguments[0].click();",chap)
            time.sleep(1)

            # 获取主窗口div的class属性判断是否点开文章
            windowClass = dr.find_element_by_xpath('//*[@id="app"]/div/div/div[1]').get_attribute('class')

            # 如果主界面div不等于12，说明没打开文件
            if windowClass != 'ivu-col ivu-col-span-12':         
                print(f'文章未打开！:{File.fileName}、{File.fileNum}')

            # 获取正文
            File.fileText = dr.find_element_by_id('docHtml').text

            # 第一个副窗口的关闭按钮
            closeBtn = dr.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div/div[1]/div/div/div[1]/div/div[2]/div/button[3]/span')

            # print(f'COOKIES:\n{dr.get_cookies()}\n')
            print(f'文章标题:\n{File.fileName}\n文章文号:\n{File.fileNum}\n文章正文:\n{File.fileText}\n\n')
            time.sleep(1)

            # 关掉第一副窗口
            try:
                dr.execute_script("arguments[0].click();",closeBtn)
            except:
                for _ in range(6):
                    click_locxy(dr, 1840, 48)
                    time.sleep(1)

            time.sleep(1)
            num_file += 1
    
        startPage += 1

if __name__ == "__main__":
    run()