#!/usr/bin/env python3
from minieyes.eyny.eyny import eyny

eyny = eyny()
for page in range(0, 20):
    print('page ' + str(page))
    eyny.goto('本土電影')

    # threads
    threads = [
        thread
        for thread in eyny.waitfor('find_elements_by_tag_name', 'tbody')
        if thread.get_attribute("id").startswith('normalthread')
    ]

    # insert database
    for thread in threads:
        th = thread.find_element_by_tag_name("th")
        xst = th.find_element_by_class_name("xst")
        link = xst.get_attribute("href")
        title = xst.get_attribute("innerHTML")
        eyny.insert_or_ignore(title, link)

    # next page
    eyny.waitfor('find_element_by_link_text','下一頁').click()