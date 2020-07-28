class eyny:
    def __init__(self):
        import dbm, time, selenium
        from selenium import webdriver
        self.db = dbm.open("./eyny/db/eyny", "c")
        self.web = webdriver.Chrome()
        self.web.get("http://www05.eyny.com/index.php")
        self.web.find_element_by_link_text("登錄").click()
        while not self.web.find_element_by_name("username").is_displayed(): time.sleep(1)
        self.web.find_element_by_name("username").send_keys('chenvey2')
        self.web.find_element_by_name("password").send_keys('shenfen520')
        self.web.find_element_by_name("loginsubmit").click()
    def __del__(self):
        self.web.quit()
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
            self.waitfor('find_element_by_name','submit').click()
            self.waitfor('find_element_by_link_text','本土電影(上傳空間)').click()
        elif where == '日韓電影':
            self.web.get("http://www05.eyny.com/forum-576-1.html")
            self.waitfor('find_element_by_name','submit').click()
            self.waitfor(self.web,'link_text','日韓電影(上傳空間)').click()
        else:
            self.web.get(where)
    def confirm18(self):
        import time
        submit = [
            tag
            for tag in self.waitfor('find_elements_by_tag_name', 'input')
            if '18歲' in tag.get_attribute('value')
        ]
        if len(submit):
            submit[0].click()
            time.sleep(5)
    def get_mega_links(self):
        # check url
        def is_valid_url(url):
            if url.startswith('https://mega.nz'): return True
            if url.startswith('https://katfile.com'): return True
            if url.startswith('https://drives.google'): return True
            return False
        return [
            val.get_attribute('href')
            for val in self.web.find_elements_by_tag_name('a')
            if val.get_attribute('href') != None and is_valid_url(val.get_attribute('href'))
        ] + [
            line
            for td in self.web.find_elements_by_tag_name('td')
            for line in td.text.split('\n')
            if 'https://' in line and is_valid_url(line[line.index('https://'):])
        ]
    def get_passwords(self):
        return [
            line
            for td in self.web.find_elements_by_tag_name('td')
            for line in td.text.split('\n')
            if '解壓密碼' in line
        ]