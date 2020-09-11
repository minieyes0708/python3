#!/usr/bin/env python3
from minieyes.eyny.eyny import eyny

eyny_local = eyny()
eyny_local.goto('本土電影')
for page in range(0, 20):
    print('page ' + str(page))

    # threads
    threads = [
        thread
        for thread in eyny_local.waitfor('find_elements_by_tag_name', 'tbody')
        if thread.get_attribute("id").startswith('normalthread')
    ]

    # insert database
    for thread in threads:
        th = thread.find_element_by_tag_name("th")
        xst = th.find_element_by_class_name("xst")
        link = xst.get_attribute("href")
        title = xst.get_attribute("innerHTML")
        eyny_local.insert_or_ignore(title, link)

    # next page
    eyny_local.waitfor('find_element_by_link_text', '下一頁').click()

eyny_japan = eyny()
eyny_japan.goto('日韓電影')
for page in range(0, 20):
    print('page ' + str(page))

    # threads
    threads = [
        thread
        for thread in eyny_japan.waitfor('find_elements_by_tag_name', 'tbody')
        if thread.get_attribute("id").startswith('normalthread')
    ]

    # insert database
    for thread in threads:
        th = thread.find_element_by_tag_name("th")
        xst = th.find_element_by_class_name("xst")
        link = xst.get_attribute("href")
        title = xst.get_attribute("innerHTML")
        eyny_japan.insert_or_ignore(title, link)

    # next page
    eyny_japan.waitfor('find_element_by_link_text', '下一頁').click()
