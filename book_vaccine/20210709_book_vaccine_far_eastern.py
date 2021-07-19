class book_vaccine:
    def __init__(self):
        from selenium import webdriver
        self.web = webdriver.Chrome()
        self.web.get('https://hos.femh.org.tw/newfemh/webreg_net/vacccontent.aspx')
    def reload(self):
        self.web.get('https://hos.femh.org.tw/newfemh/webreg_net/vacccontent.aspx')
    def fill_weiru(self):
        self.send_keys('TextBox_ID', 'R223756388')
        self.send_keys('TextBox_name', '王偉如')
        self.select('DropDownList_BirthdayYear', '079', '出生年錯誤')
        self.select('DropDownList_BirthdayMonth', '03', '出生月錯誤')
        self.select('DropDownList_BirthdayDay', '23', '出生日錯誤')
        self.click('Button4', '生日檢核錯誤')
        self.send_keys('txt_tel', '0911610105')
        self.select('DropDownList3', '2', '劑次錯誤')
        self.click('RadioButtonList1_0', '自我評估表1錯誤')
        self.click('RadioButtonList2_0', '自我評估表2錯誤')
        self.click('RadioButtonList3_0', '自我評估表3錯誤')
        self.click('RadioButtonList4_0', '自我評估表4錯誤')
        self.click('RadioButtonList5_0', '自我評估表5錯誤')
    def click(self, element_id, err_msg):
        import selenium
        try:
            self.web.find_element_by_id(element_id).click()
        except selenium.common.exceptions.NoSuchElementException:
            print('No Such Element' + element_id)
            print(err_msg)
        except:
            print('unknown error when click ' + element_id)
            print(err_msg)
    def select(self, element_id, value, err_msg):
        import selenium
        from selenium.webdriver.support.ui import Select
        try:
            Select(self.web.find_element_by_id(element_id)).select_by_value(value)
        except selenium.common.exceptions.NoSuchElementException:
            print('No Such Element: ' + element_id)
            print(err_msg)
        except:
            print('unknown error when select ' + element_id)
            print(err_msg)
    def send_keys(self, element_id, content):
        element = self.waitfor('find_element_by_id', element_id)
        element.clear()
        element.send_keys(content)
    def waitfor(self, attrname, *args):
        import time
        import selenium
        while True:
            try:
                return self.web.__getattribute__(attrname)(*args)
            except selenium.common.exceptions.NoSuchElementException:
                print(f'waiting for {attrname} ' + ' '.join(str(v) for v in args))
                time.sleep(1)
            except:
                raise

if __name__ == '__main__':
    import sys

    booker = book_vaccine()
    if len(sys.argv) > 1:
        if sys.argv[1] == 'weiru':
            booker.fill_weiru()
    else:
        import tkinter as tk
        window = tk.Tk()
        window.geometry('300x200')
        tk.Button(window, text='Reload', fg='red', command = booker.reload).pack()
        tk.Button(window, text='輸入偉如資料', command = booker.fill_weiru).pack()
        window.mainloop()
