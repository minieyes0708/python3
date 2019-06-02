import time
from selenium import webdriver

with open('reserved.txt', 'r') as file:
    reserved = set([int(stock_id.strip()) for stock_id in file.readlines()])

web = webdriver.Chrome()

while len(reserved) != 0:
    print(len(reserved))
    stock_id = reserved[0]
    web.get('http://www.cmoney.tw/finance/f00025.aspx?s={0}'.format(stock_id))
    web.find_element_by_link_text('K線').click()
    web.execute_script("window.scrollTo(0,250);"); time.sleep(5)
    web.get_screenshot_as_file('reserved/%04d.png' % (stock_id))
    del reserved[0]

web.quit()
