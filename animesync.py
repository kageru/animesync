#!/usr/bin/env python3

import config2
import pysftp
import os
import re

# broken, and I also don’t really care about the resolution tag
# filepattern = re.compile(r'(\[(?P<tag>.*)\])?\s?(?P<anime>.*)\s?[-–—]\s?(?P<episode>\d+)\s?([([](?P<resolution>\d{2,5}p?)[)\]])?\s?(\[(?P<crc>[0-9a-fA-F]{6})\])?\.(mkv|mp4)')
filepattern = re.compile(r'(\[(?P<tag>.*)\])?\s?(?P<title>.*?)\s?[-–—]\s?(?P<episode>\d+).*\.(mkv|mp4)')


def get_remote_filelist(conn: pysftp.Connection) -> list:
    return conn.listdir()


def parse_filename(filename):
    return re.match(filepattern, filename)


def local_file_exists(file):
    return os.path.isfile(os.path.join(config2.local_directory, ))



def download_file(file):
    pass


if __name__ == '__main__':
    with pysftp.Connection(host=config2.ftp_host, username=config2.ftp_user, private_key=config2.ftp_key) as conn:
        with conn.cd(config2.remote_directory):
            files = get_remote_filelist(conn)
            for file in files:
                print(file)
                parsed = parse_filename(str(file))
                if not local_file_exists(parsed):
                    download_file(parsed)
