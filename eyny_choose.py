from selenium import webdriver
import dbm, re, os, time, codecs, urllib.request

if __name__ == 'minieyes.eyny_choose':
    PATH = 'minieyes/'
else:
    PATH = ''
    
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

def translate(str):
    web.get('https://translate.google.com.tw/#ja/zh-TW/' +
            urllib.parse.urlencode({'p':str})[2:])
    while not len(web.find_element_by_id('result_box').get_attribute('innerHTML')): pass
    return web.find_element_by_id('result_box').get_attribute('innerHTML')

############
# database #
############
newdb = dbm.open(PATH+'eyny_new', 'c')
tododb = dbm.open(PATH+'eyny_todo', 'c')

try:
    keys = list(newdb.keys())
    index = -1
    cmd = 'n'
    while len(cmd) == 0 or cmd[0] != 'q':
        ################
        ##### help #####
        ################
        if cmd[0] == 'h':
            print('q: quit')
            print('h: help')
            print('n: next')
            print('t: todo')
            print('d: delete')
            print('l: link')
        ################
        ##### next #####
        ################
        if cmd[0] == 'n':
            if index < len(keys) - 1:
                index = index + 1
                [picture, title, link] = re.split('\|\|\|', newdb[keys[index]].decode('utf8'))
                if picture[0:4] == 'http':
                    req = urllib.request.Request(picture);
                    req.add_header('Referer', 'http://www05.eyny.com/index.php')
                    with open(PATH+'test.jpg','wb') as file:
                        file.write(urllib.request.urlopen(req).read())
                with codecs.open(PATH+'eyny.html', 'w', 'utf8') as file:
                    file.write(r"<meta http-equiv='Content-Type' content='text/html; charset=utf8'/>")
                    file.write('({0}/{1})<img src="test.jpg"/><br/>{2}<br/>'.format(index+1, len(keys), title))
                    # file.write(translate(title))
                web.get('file:///' + os.path.join(os.getcwd(), PATH, 'eyny.html'))
                web.refresh()
            else:
                print('no more data')
        ################
        ##### todo #####
        ################
        if cmd[0] == 't':
            tododb[keys[index]] = picture + '|||' + title + '|||' + link
            del newdb[keys[index]]
            print('TODO: {0}'.format(title))
        ##################
        ##### delete #####
        ##################
        if cmd[0] == 'd':
            del newdb[keys[index]]
            print('DELETE: {0}'.format(title))
        ################
        ##### link #####
        ################
        if cmd[0] == 'l':
            web.get(link)
            ##### 滿18歲 #####
            submit = [tag for tag in web.find_elements_by_tag_name('input') if re.search('18歲',tag.get_attribute('value'))]
            if len(submit): submit[0].click()
        if len(cmd) == 1: cmd = input('$ ')
        else: cmd = cmd[1:]
except:
    tododb.close()
    newdb.close()
    web.quit()
    raise

tododb.close()
newdb.close()
web.quit()
