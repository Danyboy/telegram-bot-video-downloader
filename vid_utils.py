import os
from glob import glob, escape
from subprocess import Popen, PIPE
from time import strftime, strptime, sleep
from contextlib import contextmanager

class Video:
    def __init__(self, link):
        self.link = link
        self.file_name = None
        
    def download(self):
        cmd = "yt-dlp --recode mp4 {0}".format(self.link)
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()

        for line in str(p[0], 'utf-8').split('\n'):
            if "[VideoConvertor] Converting video from webm to mp4; Destination:" in line:
                self.file_name = line[65:] # name of the file

    @contextmanager
    def send(self):
        yield self.file_name
        os.remove(self.file_name)
