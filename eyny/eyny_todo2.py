from selenium import webdriver
import dbm, re, time

#########
# login #
#########
web = webdriver.Chrome()
web.get("http://www05.eyny.com/index.php")
web.find_element_by_link_text("登錄").click()
while not web.find_element_by_name("username").is_displayed():
    time.sleep(1)
web.find_element_by_name("username").send_keys('chenvey2')
web.find_element_by_name("password").send_keys('shenfen520')
web.find_element_by_name("loginsubmit").click()

############
# database #
############
if __name__ == 'minieyes.eyny_todo':
    tododb = dbm.open(r'minieyes/eyny_todo','c')
else:
    tododb = dbm.open(r'eyny_todo','c')

try:
    keys = list(tododb.keys())
    index = -1
    cmd = input('$ ')
    while len(cmd) == 0 or cmd[0] != 'q':
        ################
        ##### help #####
        ################
        if cmd[0] == 'h':
            print('q: quit')
            print('h: help')
            print('n: next')
        ################
        ##### next #####
        ################
        if cmd[0] == 'n':
            if index < len(keys) - 1:
                index = index + 1
                [picture, title, link] = re.split('\|\|\|',tododb[keys[index]].decode('utf8'))
                web.get(link)
                ##### 滿18歲 #####
                submit = [tag for tag in web.find_elements_by_tag_name('input') if re.search('18歲',tag.get_attribute('value'))]
                if len(submit):
                    submit[0].click()
                    time.sleep(5)
                ##### 下載連結 #####
                # attachments = [tag for tag in web.find_elements_by_tag_name('a') if re.search('.*\.torrent',tag.get_attribute('innerHTML'))]
                # for ind in range(0,len(attachments)):
                #     print('{0}: {1}'.format(ind, attachments[ind].get_attribute('innerHTML')))
                # for ind in re.split(',',input('choose(用逗號分隔): ')):
                #     if ind: attachments[int(ind)].click()
                # # if input('remove (y/n)? ') == 'y':
                # print('Done & Removed: {0}'.format(title))
                input('press any key to continue')
                del tododb[keys[index]]
            else:
                print('no more data')
        if len(cmd) == 1: cmd = input('$ ')
        else: cmd = cmd[1:]
except:
    tododb.close()
    # web.quit()
    raise

tododb.close()
web.quit()
