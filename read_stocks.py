from selenium import webdriver

with open('stocks.txt', 'r') as file:
    stocks = [int(id.strip()) for id in file.readlines() if len(id) == 5]
with open('reserved.txt', 'r') as file:
    reserved = [int(id.strip()) for id in file.readlines() if len(id) == 5]

stocks.sort()
stocks = list(set(stocks).difference(reserved))

web = webdriver.Chrome()

command = ''
while command != 'q' and len(stocks) != 0:
    stock_id = stocks[0]
    web.get('http://www.cmoney.tw/finance/f00025.aspx?s=' + str(stock_id))
    web.execute_script("window.scrollTo(0,250);");
    frames = web.find_elements_by_tag_name('iframe')
    web.switch_to_frame(frames[0])
    btns = web.find_elements_by_tag_name('input')
    btns[1].click()
    web.switch_to_default_content()
    del stocks[0]
    command = input('(q to quit) (%d)(%d) >> ' % (len(stocks), stock_id))

web.quit()

with open('stocks.txt', 'w') as file:
    file.write('\n'.join([str(id) for id in stocks]))
