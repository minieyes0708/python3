#!/usr/bin/env python3
from eyny import eyny
from selenium.webdriver.common.by import By

eyny_local = eyny()
eyny_local.goto('本土電影')
for page in range(0, 20):
    print('page ' + str(page))

    # threads
    threads = [
        thread
        for thread in eyny_local.waitforall(By.TAG_NAME, 'tbody')
        if thread.get_attribute("id").startswith('normalthread')
    ]

    # insert database
    for thread in threads:
        th = thread.find_element(By.TAG_NAME, "th")
        xst = th.find_element(By.CLASS_NAME, "xst")
        link = xst.get_attribute("href")
        title = xst.get_attribute("innerHTML")
        eyny_local.insert_or_ignore(title, link)

    # next page
    eyny_local.waitfor(By.LINK_TEXT, '下一頁').click()

eyny_japan = eyny()
eyny_japan.goto('日韓電影')
for page in range(0, 20):
    print('page ' + str(page))

    # threads
    threads = [
        thread
        for thread in eyny_japan.waitforall(By.TAG_NAME, 'tbody')
        if thread.get_attribute("id").startswith('normalthread')
    ]

    # insert database
    for thread in threads:
        th = thread.find_element(By.TAG_NAME, "th")
        xst = th.find_element(By.CLASS_NAME, "xst")
        link = xst.get_attribute("href")
        title = xst.get_attribute("innerHTML")
        eyny_japan.insert_or_ignore(title, link)

    # next page
    eyny_japan.waitfor(By.LINK_TEXT, '下一頁').click()
