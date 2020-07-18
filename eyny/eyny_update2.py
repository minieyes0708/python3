#!/usr/bin/env python3

import dbm
from minieyes.eyny.eyny import eyny

web = eyny()
db = dbm.open("eyny", "c")

for page in range(0, 20):
    print('page ' + str(page))
    # threads
    threads = [
        thread
        for thread in web.waitfor('find_elements_by_tag_name', 'tbody')
        if thread.get_attribute("id").startswith('normalthread')
    ]

    # insert database
    for thread in threads:
        link = thread.find_element_by_tag_name("th").find_element_by_class_name("xst").get_attribute("href")
        title = thread.find_element_by_tag_name("th").find_element_by_class_name("xst").get_attribute("innerHTML")
        if title not in db:
            print("New Thread: " + title)
            db[title] = title + '|||' + link

    # next page
    web.waitfor('find_element_by_link_text','下一頁').click()

db.close()