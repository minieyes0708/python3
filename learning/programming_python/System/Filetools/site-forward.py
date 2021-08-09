"""
################################################################################
Create forward-link pages for relocating a web site.
Generates one page for every existing site html file; upload the generated
files to your old web site. See ftplib later in the book for ways to run
uploads in scripts either after or during page file creation.
################################################################################
"""

import os
servername = 'learning-python.com'
homedir = 'books'
sitefilesdir = r'C:\temp\public_html'
uploaddir = r'C:\temp\isp-forward'
templatename = 'template.html'

try:
    os.mkdir(uploaddir)
except OSError: pass

template = open(templatename).read()
sitefiles = os.listdir(sitefilesdir)

count = 0
for filename in sitefiles:
    if filename.endswith('.html') or filename.endswith('.htm'):
        fwdname = os.path.join(uploaddir, filename)
        print('creating', filename, 'as', fwdname)
        filetext = template.replace('$server$', servername)
        filetext = filetext.replace('$home$', homedir)
        filetext = filetext.replace('$file$', filename)
        open(fwdname, 'w').write(filetext)
        count += 1

print('Last file =>\n', filetext, sep='')
print('Done:', count, 'forward files created.')
