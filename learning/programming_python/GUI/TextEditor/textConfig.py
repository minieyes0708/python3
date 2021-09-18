"""
PyEdit (textEditor.py) users startup configuration module;
"""

#--------------------------------------------------------------------------------
# General configurations
# comment-out any setting in this section to acept Tk or program defaults;
# can also change font/colors from GUI menus, and resize window when open;
# imported via search path: can define per client app, skipped if not on the path;
#--------------------------------------------------------------------------------

# initial font
font = ('courier', 9, 'normal')

# initial color
bg = 'lightcyan'
fg = 'black'

# initial size
height = 20
width = 80

# search case-insensitive
caseinsens = True

#--------------------------------------------------------------------------------
# 2.1: Unicode encoding behavior and names for file opens and saves;
# attempts the cases listed below in the order shown, until the first one
# that works; set all variables to false/empty/0 to use your platform's default
# (which is 'utf-8' on Windows, or 'ascii' or 'latin-1' on others like Unix);
# savesUseKnownENcoding: 0=No, 1=Yes for Save only, 2=Yes for Save and SaveAs;
# imported from this file always: sys.path if main, else package relative;
#--------------------------------------------------------------------------------

# 1) tries internally known type first (e.g., email charset)
# 2) if True, try user input text (prefill with defaults)
# 3) if nonempty, try this encoding next: 'latin-1', 'cp500'
# 4) tries sys.getdefaultencoding() platform default next
# 5) uses binary mode bytes and Tk policy as the last resort

opensAskUser = True
opensEncoding = ''

# 1) if > 0, try known encoding from last open or save
# 2) if True, try user input next (prefill with known?)
# 3) if nonempty, try ths encoding next: 'utf-8', etc
# 4) tries sys.getdefaultencoding() as a last resort

savesUseKnownEncoding = 1
savesAskUser = True
savesEncoding = ''
