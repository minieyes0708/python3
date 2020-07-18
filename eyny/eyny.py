class eyny:
    def __init__(self):
        import time, selenium
        while True:
            try:
                self.web = selenium.webdriver.Chrome()
                self.web.get("http://www05.eyny.com/index.php")
                self.web.find_element_by_link_text("登錄").click()
                while not self.web.find_element_by_name("username").is_displayed(): time.sleep(1)
                self.web.find_element_by_name("username").send_keys('chenvey2')
                self.web.find_element_by_name("password").send_keys('shenfen520')
                self.web.find_element_by_name("loginsubmit").click()
            except:
                raise
    def __del__(self):
        self.web.quit()
    def waitfor(self, attrname, *args):
        import time, selenium
        while True:
            try:
                return self.web.__getattribute__(attrname)(*args)
            except selenium.common.exceptions.NoSuchElementException:
                time.sleep(1)
            except:
                raise
    def goto(self, where):
        if where == '本土電影':
            self.web.get("http://www05.eyny.com/forum-576-1.html")
            self.waitfor('get_element_by_name','submit').click()
            self.waitfor('get_element_by_link_text','本土電影(上傳空間)').click()
        elif where == '日韓電影':
            self.web.get("http://www05.eyny.com/forum-576-1.html")
            self.waitfor('get_element_by_name','submit').click()
            self.waitfor(self.web,'link_text','日韓電影(上傳空間)').click()