class book_vaccine:
    def __init__(self):
        from selenium import webdriver
        self.web = webdriver.Chrome()
        self.web.get('https://www.beclass.com/rid=25463b360c2d63d77ae7')
        frame = self.waitfor('find_element_by_id', 'beclassmainframe')
        self.web.switch_to.frame(frame);
    def reload(self):
        self.web.get('https://www.beclass.com/rid=25463b360c2d63d77ae7')
        frame = self.waitfor('find_element_by_id', 'beclassmainframe')
        self.web.switch_to.frame(frame);
    def fill_lori(self):
        from selenium.webdriver.support.ui import Select
        self.send_keys('person_id', 'R223573692')
        self.send_keys('username', '王聖雰')
        self.web.find_elements_by_name('sex')[1].click()
        Select(self.web.find_element_by_id('bornyear')).select_by_value("1987")
        self.send_keys('email', 'shenfen@msn.com')
        self.send_keys('mobile', '0932871908')
        self.web.find_elements_by_name('tb_extra_0[]')[4].click()
        self.send_keys('tb_extra_1', '新竹市關新路19巷65號8樓')
    def fill_minieyes(self):
        from selenium.webdriver.support.ui import Select
        self.send_keys('person_id', 'A126364215')
        self.send_keys('username', '陳怡哲')
        Select(self.web.find_element_by_id('bornyear')).select_by_value("1985")
        self.web.find_elements_by_name('sex')[0].click()
        self.send_keys('email', 'chenvey2@gmail.com')
        self.send_keys('mobile', '0919523714')
        self.web.find_elements_by_name('tb_extra_0[]')[4].click()
        self.send_keys('tb_extra_1', '新竹市關新路19巷65號8樓')
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
                time.sleep(1)
            except:
                raise

if __name__ == '__main__':
    import sys

    booker = book_vaccine()
    if len(sys.argv) > 1:
        if sys.argv[1] == 'lori':
            booker.fill_lori()
        elif sys.argv[1] == 'minieyes':
            booker.fill_minieyes()
    else:
        import tkinter as tk
        window = tk.Tk()
        window.geometry('300x200')
        tk.Button(window, text='Reload', fg='red', command = booker.reload).pack()
        tk.Button(window, text='輸入聖雰資料', command = booker.fill_lori).pack()
        tk.Button(window, text='輸入怡哲資料', command = booker.fill_minieyes).pack()
        window.mainloop()
