from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import time


n = 1
def get_page(url , shop):
    # options = webdriver.ChromeOptions()
    # #不加载图片，提升速度
    # options.add_experimental_option('prefs' , {"profile.managed_default_content_settings.images": 2})

    driver = webdriver.Chrome('chromedriver.exe' , options=options)
    driver.get(url)
    input_ = driver.find_element_by_xpath('//*[@id="key"]')
    button = driver.find_element_by_xpath('//*[@id="search"]/div/div[2]/button')
    input_.send_keys(shop)
    button.click()
    get_data(driver)


def get_data(page):
    global n
    #数据保存列表
    db_list = []
    excel_list = []
    time.sleep(3)
    #滑到页面底部（执行js脚本）
    js = "window.scrollTo(0,10000)" 
    page.execute_script(js)
    # time.sleep(2)
    #智能等待页面加载完成
    try:
        WebDriverWait(page ,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="J_goodsList"]/ul/li[20]/div/div[7]/span/a')))
    except:
        print('timeout')
    datas = page.find_element_by_xpath('//*[@id="J_goodsList"]/ul') # 一页60件
    try:
        for i in range(1,60):
            name = page.find_element_by_xpath('//*[@id="J_goodsList"]/ul/li[{}]/div/div[4]/a/em'.format(i)).text  #商品名称
            price = page.find_element_by_xpath('//*[@id="J_goodsList"]/ul/li[{}]/div/div[3]/strong/i'.format(i)).text  #商品价格
            strong = page.find_element_by_xpath('//*[@id="J_goodsList"]/ul/li[{}]/div/div[5]/strong'.format(i)).text  #评价数
            shop_name = page.find_element_by_xpath('//*[@id="J_goodsList"]/ul/li[{}]/div/div[7]/span/a'.format(i)).text #店铺名
            try:
                good_icons = page.find_element_by_xpath('//*[@id="J_pro_100008348542"]').text.replace('\n','') #是否自营
            except:
                good_icons = '无'
            #保存到列表   
            db_list.append({'商品名称':name , '商品价格':price , '评论数':strong , '店铺名': shop_name , '其它信息': good_icons})
            excel_list.append([name , price , strong , shop_name , good_icons])
    except Exception as e:
        print(e)
        pass

    save_mongodb(db_list)
    # save_excel(excel_list)
    print('save {} is ok!'.format(n))
    n += 1
    # 翻页
    click_next(page)
    get_data(page)

def click_next(page):
    next = page.find_element_by_xpath('//*[@id="J_bottomPage"]/span[1]/a[9]')
    next.click()

def save_mongodb(li):
    link = MongoClient()
    database = link['ko']['data1']
    database.insert(li)
    # database.remove({}) #清空表

def save_excel(li):
    with open('./data/京东商品.csv','a',encoding = 'utf-8-sig') as f:
        for i in li:
            f.write(','.join(i)+ '\n')

if __name__ == "__main__":
    save_excel([['商品名称','商品价格','评论数','店铺名' , '其它信息']])
    url = 'https://www.jd.com/'
    shop = '手机'
    get_page(url , shop)
    # save_mongodb([1])
    
    