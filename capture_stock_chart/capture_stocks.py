def capture_stocks():
    import time
    from selenium import webdriver

    with open('reserved.txt', 'r') as file:
        reserved = set([stock_id.strip() for stock_id in file.readlines()])
    with open('stocks.txt', 'r') as file:
        stocks =list(set([stock_id.strip() for stock_id in file.readlines()]).difference(reserved))

    web = webdriver.Chrome()

    while len(stocks) != 0:
        print(len(stocks))
        stock_id = stocks[0]
        web.get('http://www.cmoney.tw/finance/f00025.aspx?s={0}'.format(stock_id))
        web.find_element_by_link_text('K線').click()
        web.execute_script("window.scrollTo(0,250);"); time.sleep(5)
        web.get_screenshot_as_file('stocks/%s.png' % (stock_id))
        del stocks[0]

    web.quit()


if __name__ == '__main__':
    capture_stocks()
