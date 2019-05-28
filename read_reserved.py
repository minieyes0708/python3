import selenium
from selenium import webdriver

with open('reserved.txt', 'r') as file:
    reserved = [int(id.strip()) for id in file.readlines() if len(id) == 5]

reserved.sort()
reserved = list(set(reserved))

web = webdriver.Chrome()

while len(reserved) != 0:
    print(len(reserved))
    stock_id = reserved[0]
    web.get('http://www.cmoney.tw/finance/f00025.aspx?s=' + str(stock_id))
    web.find_element_by_link_text('K線').click()
##    frames = web.find_elements_by_tag_name('iframe')
##    for frame_ind in range(len(frames)):
##        try:
##            web.switch_to_frame(frames[frame_ind])
##            btns = [btn for btn in web.find_elements_by_tag_name('input')
##                    if btn.get_attribute('value') == '周線']
##            if len(btns) != 0:
##                btns[0].click()
##                break
##        except selenium.common.exceptions.StaleElementReferenceException as err:
##            pass
##    web.switch_to_default_content()
    web.execute_script("window.scrollTo(0,250);");
    web.get_screenshot_as_file('reserved/%04d.png' % (stock_id))
    del reserved[0]

web.quit()
