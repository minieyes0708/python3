from selenium import webdriver
import dbm, re, time, selenium

#########
# login #
#########
def start_and_login():
    while True:
        try:
            web = webdriver.Chrome()
            web.get("http://www05.eyny.com/index.php")
            web.find_element_by_link_text("登錄").click()
            while not web.find_element_by_name("username").is_displayed():
                time.sleep(1)
            web.find_element_by_name("username").send_keys('chenvey2')
            web.find_element_by_name("password").send_keys('shenfen520')
            web.find_element_by_name("loginsubmit").click()
            return web
        except:
            web.quit()

def get_mega_links(web):
    url = [val.get_attribute('href') for val in web.find_elements_by_tag_name('a') if 'mega' in val.text and 'https://mega.nz' in val.get_attribute('href')]
    groups = [re.search('【影片載點】：([^\n]+)', val.text) for val in web.find_elements_by_tag_name('td') if '影片載點' in val.text]
    url.extend([grp.group(1) for grp in groups if grp != None and grp.groups != None and 'https://mega.nz' in grp.group(1)])
    return url

def get_passwords(web):
    result = []
    groups = [re.search('【解壓密碼】：([^\n]+)', val.text) for val in web.find_elements_by_tag_name('td') if '解壓密碼' in val.text]
    return [grp.group(1) for grp in groups if grp != None and grp.groups != None]

############
# database #
############
if __name__ == 'minieyes.eyny_todo':
    tododb = dbm.open(r'minieyes/eyny_new','c')
else:
    tododb = dbm.open(r'eyny_new','c')

count = 0
max_count = -1
while True:
    try:
        web = start_and_login()
        keys = list(tododb.keys())
        index = 0
        while index < len(keys):
            [picture, title, link] = re.split('\|\|\|',tododb[keys[index]].decode('utf8'))
            web.get(link)
            ##### 滿18歲 #####
            submit = [tag for tag in web.find_elements_by_tag_name('input') if re.search('18歲',tag.get_attribute('value'))]
            if len(submit):
                submit[0].click()
                time.sleep(5)
            ##### print連結/密碼 #####
            url = get_mega_links(web)
            print('========== ' + str(index) + '/' + str(len(keys)) + ' ==========' + '\n')
            if len(url) != 0:
                file = open('todo_filter.txt', 'a')
                file.write('========== ' + str(index) + '/' + str(len(keys)) + ' ==========' + '\n')
                file.write('link = ' + link + '\n')
                file.write('\n'.join(url) + '\n')
                file.write('\n'.join(get_passwords(web)) + '\n')
                file.close()
                count = count + 1
            del tododb[keys[index]]
            index = index + 1
        break
    except selenium.common.exceptions.TimeoutException:
        print('Time Out')
        web.quit()
        next
    except:
        tododb.close()
        # web.quit()
        raise
    if count == max_count: break

tododb.close()
web.quit()
