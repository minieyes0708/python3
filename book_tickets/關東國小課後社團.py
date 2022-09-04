from selenium import webdriver
from selenium.webdriver.common.by import By

import tkinter as tk
web = webdriver.Chrome()

UserName = '陳以恩'
JobTitle = '1年15班'
Mobile = '0932871908'
PhoneArea = '03'
PhoneBody = '5001889'
PhoneExt = '26918'
Email = 'chenvey2@gmail.com'

def BackToHomePage():
    web.get('https://www.beclass.com/rid=2648b9e630dad3ba65e6')
    web.switch_to.frame(1)

def FillInput(input_id, content):
    element = web.find_element(By.ID, input_id)
    element.clear()
    element.send_keys(content)

def ClickRatio(group_name, radio_value):
    elements = web.find_elements(By.NAME, group_name)
    [el for el in elements if el.get_attribute('value') == radio_value][0].click()

def FillUserInfo():
    FillInput('username', UserName)
    FillInput('job_title', JobTitle)
    ClickRatio('sex', '男')
    FillInput('mobile', Mobile)
    FillInput('phone_area', PhoneArea)
    FillInput('phone_body', PhoneBody)
    FillInput('phon_ext', PhoneExt)
    FillInput('email', Email)

BackToHomePage()
window = tk.Tk()
window.title('關東國小課後社團')
btnHome = tk.Button(
    window,
    text = '重連主頁',
    width = 20, height = 2,
    command = BackToHomePage,
    fg = 'red')
btnHome.pack()
btnUserInfo = tk.Button(
    window,
    text = '輸入個人資訊',
    width = 20, height = 2,
    command = FillUserInfo)
btnUserInfo.pack()
window.attributes("-topmost", True)
window.mainloop()

web.quit()
