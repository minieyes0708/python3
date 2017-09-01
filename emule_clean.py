import os, re, stat

EMULE = r'J:\tmp\emule'
TOPDIR = [os.path.join(EMULE,folder) \
          for folder in os.listdir(EMULE)\
          if os.path.isdir(os.path.join(EMULE,folder))]
IGNORE_FOLDER = ['backup',\
                 'WANZ-331',\
                 'langxing1212@第一会所@SW-048 プリプリ若い身体の女子校生を触りたくてマッサージしてやると言ってモミまくったらブルマを濡らして欲しがった',\
                 'pppd314',\
                 'PLA-045',\
                 'MUM-102',\
                 'MIRD-012',\
                 'mimip2p+nike(MIRD012) A+B',\
                 'KAM-055',\
                 'IPZ628AVI',\
                 'IENE-181',\
                 'DOHI-021',\
                 'Akihabara Kabukicho Chiropractor Clinic',\
                 '0930晚',\
                 '',\
                 '',\
                 '',\
                 ''\
                ]
IGNORE_EXT = ['torrent','gif','chm','jpeg','mht','fb!','exe']
BACKUP_EXT = ['rar', 'mkv', 'wmv', 'mp4', 'rmvb', 'zip', 'avi','iso']

# git diff tool test

def getFileList(folder):
    files = []
    dirs = [folder]
    while len(dirs):
        dirs = dirs + [os.path.join(dirs[0],d)\
                       for d in os.listdir(dirs[0])\
                       if os.path.isdir(os.path.join(dirs[0],d))]
        files = files + [os.path.join(dirs[0],f)\
                         for f in os.listdir(dirs[0])\
                         if os.path.isfile(os.path.join(dirs[0],f))]
        del dirs[0]
    return files

def isIgnoredExt(file):
    for ext in IGNORE_EXT:
        if re.search('.*\.'+ext+'$', file):
            return True
    return False

def isBackupExt(file):
    for ext in BACKUP_EXT:
        if re.search('.*\.'+ext+'$', file):
            return True
    return False

def isIgnoredFolder(folder):
    for f in IGNORE_FOLDER:
        if re.search(r'.*\\'+re.escape(f)+'$', folder):
            return True
    return False

cmd = input('$ ')
index = -1
while cmd != 'q':
    ################
    ##### help #####
    ################
    if cmd == 'h':
        print('h: help')
        print('q: quit')
        print('n: next')
        print('d: delete')
    ################
    ##### next #####
    ################
    if cmd == 'n':
        if index < len(TOPDIR) - 1:
            # advance index
            index = index + 1
            # ignore folder
            if isIgnoredFolder(TOPDIR[index]): continue
            # get folder
            folder = TOPDIR[index]
            print('Processing Folder: {0}'.format(folder))
            # Loop Through Folder
            for file in getFileList(folder):
                #******************#
                #***** Ignore *****#
                #******************#
                if(isIgnoredExt(file)):
                    pass # print('{0:20s}\n.....ignored'.format(file))
                #******************#
                #***** Backup *****#
                #******************#
                elif(isBackupExt(file)):
                    target_file = os.path.join(EMULE, 'backup', os.path.basename(file))
                    if os.path.exists(target_file):
                        print('{0:20s}\n.....ignored since already exists'.format(target_file))
                    else:
                        print('{0:20s}\n.....backup to {1}'.format(file, os.path.join(EMULE,'backup')))
                        os.rename(file, target_file)
                #*******************#
                #***** Unknown *****#
                #*******************#
                else:
                    print('{0:20s}\n.....unknown'.format(file))
            print('===== end of file list =====')
        else:
            print('no more data')
    ##################
    ##### delete #####
    ##################
    if cmd == 'd':
        for root, dirs, files in os.walk(folder, topdown = False):
            for name in files:
                file = os.path.join(root, name)
                os.chmod(file, stat.S_IWUSR)
                os.remove(file)
            for name in dirs:  os.rmdir(os.path.join(root, name))
        os.rmdir(folder)
        print('Folder: {0} removed'.format(folder))

    if len(cmd): cmd = input('$ ')
    else: cmd = cmd[1:]
