import os
from youtube.flvretriever import flvretriever

full_path = os.path.realpath(__file__)
folder_path = os.path.split(full_path)[0]

with flvretriever() as rtvr:
    with open(os.path.join(folder_path, 'download_list.txt'), encoding='utf8') as file:
        while True:
            save_path = file.readline()
            if not save_path: break
            url = file.readline()
            if not url: break
            rtvr.search(url.strip())
            rtvr.save_to('Audio (MP4, Stereo 44KHz)', save_path.strip())
