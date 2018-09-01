from selenium import webdriver

with open('reserved.txt', 'r') as file:
    reserved = [int(id.strip()) for id in file.readlines() if len(id) == 5]

reserved.sort()
reserved = list(set(reserved))

web = webdriver.Chrome()

command = ''
while command != 'q' and len(reserved) != 0:
    web.get('http://www.cmoney.tw/finance/f00025.aspx?s=' + str(reserved[0]))
    web.execute_script("window.scrollTo(0,250);");
    del reserved[0]
    command = input('(q to quit) (%d) >> ' % (len(reserved)))

web.quit()