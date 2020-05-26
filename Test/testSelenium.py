from selenium import webdriver
from time import sleep
import requests
option = webdriver.ChromeOptions()
option.add_argument("headless")
base_url = "https://www.acfun.cn/a/ac15769393"
list=[]
imglist =[]
imglistxpath=[]
# 创建一个浏览器句柄对象
dri = webdriver.Chrome(executable_path="chromedriver.exe",chrome_options=option)
#跳转到指定url
dri.get(base_url)
sleep(3)#
#next_btn = dri.find_element_by_id("pageIto_next")

list = dri.find_elements_by_class_name("area-comment-des-content")
imglist = dri.find_elements_by_css_selector('.area-comment-des-content>img')
#imglistxpath = dri.find_elements_by_xpath("/html/body/div[2]/section/div[2]/div[1]/div/section/div/div[2]/div/div[6]/div[1]/div[1]/div/div[3]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/p/img")
print(len(list))
for item in imglist:
    print(item.get_attribute("src"))
sleep(3)
dri.quit()