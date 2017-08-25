# web driver
import selenium, time, re, dbm
from selenium import webdriver

def wait_for(web,category, name):
    while True:
        try:
            if category == 'name':
                element = web.find_element_by_name(name)
            elif category == 'link_text':
                element = web.find_element_by_link_text(name)
            elif category == 'tag_names':
                element = web.find_elements_by_tag_name(name)
            else:
                raise NameError('Unknown category: ' + category)
            return element
        except selenium.common.exceptions.NoSuchElementException:
            time.sleep(1)
        except:
            raise

def initialize(web, url):
    web.get("http://www05.eyny.com/index.php")
    # login
    login = web.find_element_by_link_text("登錄").click()
    while not web.find_element_by_name('username').is_displayed():
        time.sleep(1)
    web.find_element_by_name("username").send_keys('chenvey2')
    web.find_element_by_name("password").send_keys('shenfen520')
    web.find_element_by_name("loginsubmit").click()
    if url == None:
        web.get("http://www05.eyny.com/forum-576-1.html");
        (wait_for(web,'name','submit')).click()
        # (wait_for(web,'link_text','本土電影(上傳空間)')).click()
        (wait_for(web,'link_text','日韓電影(上傳空間)')).click()
    else:
        web.get(url)
        (wait_for(web,'name','submit')).click()

db = dbm.open("eyny", "c")
newdb = dbm.open("eyny_new", "c")

page = 0
web = None
url = None
min_page = 0
while page < 20:
    print('page ' + str(page))
    while True:
        try:
            if web == None:
                web = webdriver.Chrome()
                initialize(web, url)
            if page >= min_page:
                # threads
                threads = wait_for(web,'tag_names', 'tbody')
                threads = [thread for thread in threads if(re.search("^normalthread",thread.get_attribute("id")))]

                # insert database
                for thread in threads:
                    link = thread.find_element_by_tag_name("th").find_element_by_class_name("xst").get_attribute("href")
                    title = thread.find_element_by_tag_name("th").find_element_by_class_name("xst").get_attribute("innerHTML")
                    picture = thread.find_element_by_class_name("p_pre_td").find_elements_by_class_name("p_pre_none")
                    if len(picture): picture = picture[0].get_attribute("src")
                    else: picture = ""
                    thread_id = re.search("thread-(.*)\.html", link).group(1)
                    if title not in db:
                        print("New Thread: " + title)
                        db[title] = picture + '|||' + title + '|||' + link
                        newdb[thread_id] = picture + '|||' + title + '|||' + link

            # next page
            (wait_for(web,'link_text',"下一頁")).click()
            url = web.current_url
            page = page + 1
            break
        except selenium.common.exceptions.StaleElementReferenceException:
            print('StaleElement')
            next
        except selenium.common.exceptions.TimeoutException:
            print('Timeout')
            if web != None:
                web.quit()
                web = None
            next

newdb.close();
db.close()
web.quit()
