#!/usr/bin/env python3
from minieyes.eyny.eyny import eyny

eyny = eyny()
total = eyny.count()
for index, title, link in eyny.loop_and_remove():
    eyny.goto(link)
    eyny.confirm18()

    url, passwd = eyny.get_mega_links(), eyny.get_passwords()
    urls, passwds = '\n'.join(url), '\n'.join(passwd)

    print('========== %d/%d ==========\n' % (index, total))
    if len(url) != 0:
        file = open('./minieyes/enyn/todo_filter.txt', 'a')
        file.write(
            '========== %d/%d ==========\nlink = %s\n%s\n%s\n' %
            (index, total, link, urls, passwds))
        file.close()
        print('link = %s\n%s\n%s\n' % (link, urls, passwds))
