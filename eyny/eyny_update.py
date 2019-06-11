# web driver
import selenium
from selenium import webdriver
web = webdriver.Chrome()

# home page
web.get("http://www05.eyny.com/index.php")

#########
# login #
#########
import time, re
login = web.find_element_by_link_text("登錄").click()
while not web.find_element_by_name('username').is_displayed():
    time.sleep(1)


web.find_element_by_name("username").send_keys('chenvey2')
web.find_element_by_name("password").send_keys('shenfen520')
web.find_element_by_name("loginsubmit").click()

# target page
web.find_element_by_link_text("BT日韓成人電影").click()
while True:
    try:
        web.find_element_by_name("submit").click()
        break;
    except selenium.common.exceptions.NoSuchElementException:
        web.find_element_by_link_text("BT日韓成人電影").click()
        print('NoSuchElementException')
        time.sleep(1)

import dbm, re
if __name__ == 'minieyes.eyny_update':
    db = dbm.open("minieyes/eyny", "c")
    newdb = dbm.open("minieyes/eyny_new", "c")
else:
    db = dbm.open("eyny", "c")
    newdb = dbm.open("eyny_new", "c")

try:
    for page in range(0,20):
        # threads
        while True:
            try:
                threads = web.find_elements_by_tag_name("tbody");
                threads = [thread for thread in threads if(re.search("^normalthread",thread.get_attribute("id")))]
                break;
            except selenium.common.exceptions.StaleElementReferenceException:
                print("StaleElementReferenceException")
                time.sleep(1)
            except selenium.common.exceptions.TimeoutException:
                print("TimeoutException")
                time.sleep(1)

        # insert database
        for thread in threads:
            link = thread.find_element_by_tag_name("th").find_element_by_class_name("xst").get_attribute("href")
            title = thread.find_element_by_tag_name("th").find_element_by_class_name("xst").get_attribute("innerHTML")
            picture = thread.find_element_by_class_name("p_pre_td").find_elements_by_class_name("p_pre_none")
            if len(picture): picture = picture[0].get_attribute("src")
            else: picture = ""
            thread_id = re.search("thread-(.*)\.html", link).group(1)
            if thread_id + 'link' not in db:
                print("New Thread: " + title)
                db[thread_id] = picture + '|||' + title + '|||' + link
                newdb[thread_id] = picture + '|||' + title + '|||' + link

        # next page
        web.find_element_by_link_text("下一頁").click()
except:
    newdb.close();
    db.close()
    web.quit()
    raise

newdb.close();
db.close()
web.quit()
