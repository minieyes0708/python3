import os, shutil, statementdog
from selenium.webdriver.common.by import By

# monthly-revenue-yoy url
url = 'https://statementdog.com/analysis/{}/long-term-and-short-term-monthly-revenue-yoy'

# create empty output directory
dirname = 'monthly-revenue-yoy'
if os.path.exists(dirname):
    shutil.rmtree(dirname)
os.mkdir(dirname)

# login to statementdog
dog = statementdog.statementdog().login()
dog.web.maximize_window()

# get stock id list
dog.waitfor(By.CLASS_NAME, 'stock-list')
stock_ids = [
    item.text.split()[0] for item in
    dog.web.find_elements(By.CLASS_NAME, 'stock-id-name')]

# capture monthly-revenue-yoy
for stock_id in stock_ids:
    print('goto {}'.format(stock_id))
    dog.web.get(url.format(stock_id))
    # wait for report shown up before capturing
    dog.waitfor(By.ID, 'report')
    dog.web.save_screenshot(os.path.join(dirname, stock_id+'.jpg'))
dog.web.quit()