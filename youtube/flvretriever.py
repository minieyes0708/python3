class flvretriever:
    def __init__(self):
        from selenium import webdriver
        self.web = webdriver.Chrome()
        self.reset()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.web.quit()
    def reset(self):
        self.web.get('http://kej.tw/flvretriever/')
    def search(self, url):
        self.web.find_element_by_name('videoUrl').send_keys(url)
        self.web.find_element_by_id('btnsubmit').click()
    def save_to(self, link_text, save_path):
        import urllib.request
        links = self.web.find_elements_by_tag_name('a')
        for link in links:
            if link_text in link.text:
                url = link.get_attribute('href')
                print(f'位址為{url}')
                print(f'儲存{save_path}中...')

                CHUNK = 16 * 1024
                response = urllib.request.urlopen(url)
                with open(save_path, 'wb') as file:
                    while True:
                        chunk = response.read(CHUNK)
                        if not chunk: break
                        file.write(chunk)

                print(f'儲存{save_path}完成...')
                break
    def waitfor(self, attrname, *args):
        import time
        import selenium
        while True:
            try:
                return self.web.__getattribute__(attrname)(*args)
            except selenium.common.exceptions.NoSuchElementException:
                print('waiting for ' + attrname + ' ' + ' '.join(str(v) for v in args))
                time.sleep(1)
            except:
                raise
