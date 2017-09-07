import os, shutil

def listext():
    result = []
    for root, subdirs, files in os.walk('.'):
        for file in files:
            result = result + [file[file.rfind('.'):]]
    result.sort()
    print([e for i, e in enumerate(result) if result.index(e) == i])

def filterext(ext):
    result = []
    for root, subdirs, files in os.walk('.'):
        for file in files:
            if file[file.rfind('.'):] == ext:
                result = result + [os.path.join(root,file)]
    return result

def moveext(exts):
    for ext in exts:
        for file in filterext(ext):
            print('moving ' + file)
            name = os.path.basename(file)
            shutil.move(file, os.path.join(r'J:\tmp\emule', name))

def removeext(exts):
    for ext in exts:
        for file in filterext(ext):
            os.remove(file)

def clear_empty_folders():
    for root, subdirs, files in os.walk('.', topdown=False):
        if root != '.':
            if len(subdirs) == 0:
                os.rmdir(root)

os.chdir('D:\\Downloads')
