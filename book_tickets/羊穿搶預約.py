import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select

import tkinter as tk

IdNumber = 'R223573692'
Phone = '0932871908'
Name = '王聖雰'
BirthYear = '1987'
BirthMonth = '01'
BirthDay = '13'

web = webdriver.Chrome()
web.get("http://genephile.vision.com.tw/ScheduleRegis.aspx")

def BackToHomePage():
    web.get("http://genephile.vision.com.tw/ScheduleRegis.aspx")

def BookTicket():
    pass

def FillUserInfo():
    div = web.find_element_by_class_name('regis-act-form')
    table = div.find_element_by_tag_name('table')
    trs = table.find_elements_by_tag_name('tr')
    tds6 = trs[6].find_elements_by_tag_name('td')
    tds7 = trs[7].find_elements_by_tag_name('td')
    id_input = tds6[1].find_element_by_tag_name('input')
    id_input.clear()
    id_input.send_keys(IdNumber)
    selects = tds6[3].find_elements_by_tag_name('select')
    Select(selects[0]).select_by_visible_text(BirthYear)
    Select(selects[1]).select_by_visible_text(BirthMonth)
    Select(selects[2]).select_by_visible_text(BirthDay)
    name_input = tds7[1].find_element_by_tag_name('input')
    name_input.clear()
    name_input.send_keys(Name)
    phone_input = tds7[3].find_element_by_tag_name('input')
    phone_input.clear()
    phone_input.send_keys(Phone)


window = tk.Tk()
window.title('羊穿搶預約')
btnHome = tk.Button(
    window,
    text = '重連主頁',
    width = 20, height = 2,
    command = BackToHomePage,
    fg = 'red')
btnHome.pack()
btnBook = tk.Button(
    window,
    text = '選擇日期',
    width = 20, height = 2,
    command = BookTicket)
btnBook.pack()
btnUserInfo = tk.Button(
    window,
    text = '輸入個人資訊',
    width = 20, height = 2,
    command = FillUserInfo)
btnUserInfo.pack()
window.attributes("-topmost", True)
window.mainloop()
