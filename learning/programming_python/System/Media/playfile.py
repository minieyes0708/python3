#!/usr/local/bin/python
"""
################################################################################
Try to play an arbitrary media file. Allows for specific players instead of
always using general web browser scheme. May not work on your system as is;
audio files use filters and command lines on Unix, and filename associations
on Windows via the start command (i.e., whatever you have on your machine to
run .au files--an audio player, or perhaps a web browser). Configure and
extend as needed. playknownfile assumes you know what sort of media you wish
to open, and playfile tries to determine media type automatically using Python
mimetypes module; both try to launch a webbrowser with Python webbrowser module
as a last resort when mimetype or platform unknown.
################################################################################
"""

import os, sys, mimetypes, webbrowser

helpmsg = """
Sorry: can't find a media player for '%s' on your system!
Add an entry for your system to the media player dictionary
for this type of file in playfile.py, or play the file manually.
"""

def trace(*args): print(*args)

################################################################################
# player techniques: generic and otherwise: extend me
################################################################################

class MediaTool:
    def __init__(self, runtext=''):
        self.runtext = runtext
    def run(self, mediafile, **options):
        fullpath = os.path.abspath(mediafile)
        self.open(fullpath, **options)
class Filter(MediaTool):
    def open(self, mediafile, **ignored):
        media = open(mediafile, 'rb')
        player = os.popen(self.runtext, 'w')
        player.write(media.read())
class Cmdline(MediaTool):
    def open(self, mediafile, **ignored):
        cmdline = self.runtext % mediafile
        os.system(cmdline)
class Winstart(MediaTool):
    def open(self, mediafile, wait=False, **other):
        if not wait:
            os.startfile(mediafile)
        else:
            os.system('start /WAIT ' + mediafile)
class Webbrowser(MediaTool):
    # file:// requires abs path
    def open(self, mediafile, **options):
        webbrowser.open_new('file://%s' % mediafile, **options)

################################################################################
# media- and platform-specific policies: change me, or press one in
################################################################################

# map platform to player: change me!

audiotools = {
        'sunos5': Filter('/usr/bin/audioplay'),
        'linux2': Cmdline('cat %s > /dev/audio'),
        'snuos4': Filter('usr/demo/SOUND/play')
        'win32': Winstart()
        #'win32': Cmdline('start %s')
        }

videotools = {
        'linux2': Cmdline('tkcVideo_c700 %s'),
        'win32': Winstart(),
        }

imagetools = {
        'linux2': Cmdline('zimager %s'),
        'win32': Winstart(),
        }

texttools = {
        'linux2': Cmdline('vi %s'),
        'win32': Cmdline('notepad %s')
        }

apptools = {
        'win32': Winstart()
        }

# map mimetype of filenames to player tables

mimetable = {
        'audio': audiotools,
        'video': videotools,
        'image': imagetools,
        'text': texttools,
        'application': apptools}

################################################################################
# top-level interfaces
################################################################################

def trywebbrowser(filename, helpmsg=helpmsg, **options):
    """
    try to open a file in a web browser
    last resort if unknown mimetype or platform, and for text/html
    """
    trace('trying browser', filename)
    try:
        player = Webbrowser()
        player.run(filename, **options)
    except:
        print(helpmsg % filename)
def playknownfile(filename, playertable={}, **options):
    """
    play media file of known type: uses platform-specific
    player objects, or spawns a web browser if nothing for
    this platform; accepts a media-specific player table
    """
    if sys.platform in playertable:
        playertable[sys.platform].run(filename, **options)
    else:
        trywebbrowser(filename, **options)
def playfile(filename, mimetable=mimetable, **options):
    """
    play media file of any type: uses mimetypes to guess media
    type and map to platform-specific player tables; spawn web
    browser if text/html, media type unknown, or has no table
    """
    contenttype, encoding = mimetypes.guess_type(filename)
    if contenttype == None or encoding is not None:
        contenttype = '?/?'
    maintype, subtype = contenttype.split('/', 1)
    if maintype == 'text' and subtype == 'html':
        trywebbrowser(filename, **options)
    elif maintype in mimetable:
        playknownfile(filename, mimetable[maintype], **options)
    else:
        trywebbrowser(filename, **options)

################################################################################
# self-test code
################################################################################

if __name__ == '__main__':
    # media type known
    playknownfile('sousa.au', audiotools, wait=True)
    playknownfile('ora-pp3e.gif', imagetools, wait=True)
    playknownfile('ora-lp4e.jpg', imagetools)

    # media type guessed
    input('Stop players and press Enter')
    playfile('ora-lp4e.jpg')
    playfile('ora-pp3e.gif')
    playfile('priorcalendar.html')
    playfile('lp4e-preface-preview.html')
    playfile('lp-code-readme.txt')
    playfile('spam.doc')
    playfile('spreadsheet.xls')
    playfile('sousa.au', wait=True)
    input('Done')
