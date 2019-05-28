import selenium, time
from selenium import webdriver

with open('stocks.txt', 'r') as file:
    stocks = [int(id.strip()) for id in file.readlines() if len(id) == 5]
with open('reserved.txt', 'r') as file:
    reserved = [int(id.strip()) for id in file.readlines() if len(id) == 5]

stocks.sort()
stocks = list(set(stocks).difference(reserved))

web = webdriver.Chrome()
##web.get('http://www.cmoney.tw/finance/f00025.aspx?s=' + str(3034))
##time.sleep(5)

while len(stocks) != 0:
    print(len(stocks))
    stock_id = stocks[0]
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
    web.execute_script("window.scrollTo(0,250);"); time.sleep(5)
    web.get_screenshot_as_file('stocks/%04d.png' % (stock_id))
    del stocks[0]

web.quit()

##with open('stocks.txt', 'w') as file:
##    file.write('\n'.join([str(id) for id in stocks]))

# vim: expandtab
