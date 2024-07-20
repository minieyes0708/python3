from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class eyny:
    def __init__(self):
        import dbm, time, getpass
        from selenium import webdriver
        self.db = dbm.open("./eyny/db/eyny", "c")
        self.web = webdriver.Chrome()
        self.web.get("http://www05.eyny.com/index.php")
        self.web.find_element(By.LINK_TEXT, "登錄").click()
        while not self.web.find_element(By.NAME, "username").is_displayed():
            time.sleep(1)
        self.web.find_element(By.NAME, "username").send_keys('chenvey2')
        self.web.find_element(By.NAME, "password").send_keys(getpass.getpass('密碼: '))
        Select(self.web.find_element(By.NAME, 'questionid')).select_by_index(1)
        self.web.find_element(By.NAME, "answer").send_keys(getpass.getpass('母親名字: '))
        self.web.find_element(By.NAME, "loginsubmit").click()
        time.sleep(5)
    def __del__(self):
        # self.web.quit()
        self.db.close()
    def insert_or_ignore(self, title, link):
        if title not in self.db:
            print("New Thread: " + title)
            self.db[title] = link
    def loop_and_remove(self):
        keys = self.db.keys()
        for i in range(len(keys)):
            key = keys[i]
            val = self.db[key].decode('utf8')
            yield (i, key, val)
            del self.db[key]
    def count(self):
        return len(self.db.keys())
    def waitforall(self, by, *args):
        import time
        start = time.time()
        while True:
            try:
                return self.web.find_elements(by, *args)
            except:
                raise
    def waitfor(self, by, *args):
        import time
        import selenium
        start = time.time()
        timeout = args['timeout'] if 'timeout' in args else 10
        while True:
            try:
                return self.web.find_element(by, *args)
            except selenium.common.exceptions.NoSuchElementException:
                print('waiting for ' + by + ' ' + ' '.join(str(v) for v in args))
                if time.time() - start > timeout:
                    if self.web.find_element(By.ID, 'content-title').text == '沒有這個頁面喔!':
                        raise RuntimeError('Page not found')
                time.sleep(1)
            except:
                raise
    def goto(self, where):
        if where == '本土電影':
            # self.web.get("http://www05.eyny.com/forum-576-1.html")
            self.waitfor(By.LINK_TEXT, '成人電影(上傳空間)').click()
            self.waitfor(By.LINK_TEXT, '成人電影(上傳空間)').click()
            self.waitfor(By.NAME, 'submit').click()
            self.waitfor(By.LINK_TEXT, '本土電影(上傳空間)').click()
        elif where == '日韓電影':
            # self.web.get("http://www05.eyny.com/forum-576-1.html")
            self.waitfor(By.LINK_TEXT, '成人電影(上傳空間)').click()
            self.waitfor(By.LINK_TEXT, '成人電影(上傳空間)').click()
            self.waitfor(By.NAME, 'submit').click()
            self.waitfor(By.LINK_TEXT, '日韓電影(上傳空間)').click()
        else:
            self.web.get(where)
    def confirm18(self):
        import time
        submit = [
            tag
            for tag in self.waitforall(By.TAG_NAME, 'input')
            if '18歲' in tag.get_attribute('value')
        ]
        if len(submit):
            submit[0].click()
            time.sleep(5)
    def set_mega_links(self, links):
        self.mega_links = links
    def get_mega_links(self):
        # check url
        def is_valid_url(url):
            for link_url in self.mega_links:
                if url.startswith(link_url):
                    return True
            return False
        return [
            val.get_attribute('href')
            for val in self.web.find_elements(By.TAG_NAME, 'a')
            if val.get_attribute('href') != None and is_valid_url(val.get_attribute('href'))
        ] + [
            line
            for td in self.web.find_elements(By.TAG_NAME, 'td')
            for line in td.text.split('\n')
            if 'https://' in line and is_valid_url(line[line.index('https://'):])
        ]

    def get_passwords(self):
        return [
            line
            for td in self.web.find_elements(By.TAG_NAME, 'td')
            for line in td.text.split('\n')
            if '解壓密碼' in line
        ]
