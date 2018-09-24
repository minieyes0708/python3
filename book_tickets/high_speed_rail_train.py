import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select

import tkinter as tk

StartStation = '新竹'
DestinationStation = '嘉義'

ToTimeInputField = '2018/10/21'
ToTimeTable = '09:00'

ReturnCheckBox = False      # 訂購回程?
BackTimeInputField = '2018/10/20'
BackTimeTable = '09:00'

BookMethod1 = True         # 直接輸入車次
ToTrainIdInputField = '813'

TicketAmount0 = 1          # 全票幾張?

IdNumber = 'a123456789'
MobilePhone = '0123456789'
Email = 'ASDF@msn.com'

web = webdriver.Chrome()
web.get("https://irs.thsrc.com.tw/IMINT/")

def BackToHomePage():
    web.get("https://irs.thsrc.com.tw/IMINT/")

def BookTicket():
    selectStartStation = Select(web.find_element_by_name('selectStartStation'))
    selectStartStation.select_by_visible_text(StartStation)
    selectDestationStation = Select(web.find_element_by_name('selectDestinationStation'))
    selectDestationStation.select_by_visible_text(DestinationStation)
    toTimeInputField = web.find_element_by_id('toTimeInputField')
    toTimeInputField.clear()
    toTimeInputField.send_keys(ToTimeInputField)
    if BookMethod1:
        web.find_element_by_id('bookingMethod_1').click()
        toTrainIdInputField = web.find_element_by_name('toTrainIDInputField')
        toTrainIdInputField.clear()
        toTrainIdInputField.send_keys(ToTrainIdInputField)
    else:
        toTimeTable = Select(web.find_element_by_name('toTimeTable'))
        toTimeTable.select_by_visible_text(ToTimeTable)
        returnCheckBox = web.find_element_by_id('returnCheckBox')
        if ReturnCheckBox:
            returnCheckBox.click()
            backTimeInputField = web.find_element_by_id('backTimeInputField')
            backTimeInputField.clear()
            backTimeInputField.send_keys(BackTimeInputField)
            backTimeTable = Select(web.find_element_by_name('backTimeTable'))
            backTimeTable.select_by_visible_text(BackTimeTable)
    ticketAmount0 = Select(web.find_element_by_name('ticketPanel:rows:0:ticketAmount'))
    ticketAmount0.select_by_visible_text(str(TicketAmount0))

def FillUserInfo():
    idNumber = web.find_element_by_id('idNumber')
    idNumber.clear()
    idNumber.send_keys(IdNumber)
    web.find_element_by_id('mobileInputRadio').click()
    mobilePhone = web.find_element_by_id('mobilePhone')
    mobilePhone.clear()
    mobilePhone.send_keys(MobilePhone)
    email = web.find_element_by_name('email')
    email.clear()
    email.send_keys(Email)
    web.find_element_by_name('agree').click()


window = tk.Tk()
window.title('高鐵協助訂票')
btnHome = tk.Button(
    window,
    text = '重連主頁',
    width = 20, height = 2,
    command = BackToHomePage,
    fg = 'red')
btnHome.pack()
btnBook = tk.Button(
    window,
    text = '輸入訂票資訊',
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
