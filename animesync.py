#!/usr/bin/env python3
import time

import config
import pysftp
import os
import re

# broken, and I also don’t really care about the resolution or crc tag
# filepattern = re.compile(r'(\[(?P<tag>.*)\])?\s?(?P<anime>.*)\s?[-–—]\s?(?P<episode>\d+)\s?([([](?P<resolution>\d{2,5}p?)[)\]])?\s?(\[(?P<crc>[0-9a-fA-F]{6})\])?\.(mkv|mp4)')
filepattern = re.compile(r'(\[(?P<tag>.*)\])?\s?(?P<title>.*?)\s?[-–—]\s?(?P<episode>\d+).*\.(mkv|mp4)')


def sync():
    with pysftp.Connection(host=config.ftp_host, username=config.ftp_user, private_key=config.ftp_key) as conn:
        with conn.cd(config.remote_directory):
            files = get_remote_filelist(conn)
            for file in files:
                parsed = parse_filename(file)
                if not local_file_exists(parsed):
                    download_file(conn, parsed)
                else:
                    print(f'"{file}" already exists on local system. Skipping.')
                if config.remove_files_after_download:
                    print(f'Removing "{file}" from remote server')
                    conn.remove(file)
        conn.close()


def get_remote_filelist(conn: pysftp.Connection) -> list:
    return conn.listdir()


def parse_filename(filename: str):
    return re.search(filepattern, filename)


def local_file_exists(file) -> bool:
    return os.path.isfile(os.path.join(config.local_directory, file.group('title'), file.string))


def download_file(conn: pysftp.Connection, file) -> None:
    target = os.path.join(config.local_directory, file.group('title'))
    if not os.path.exists(target):
        os.mkdir(target)
    print(f'Downloading "{file.string}" into "{target}"')
    start = time.time()
    conn.get(file.string, os.path.join(target, file.string))
    filesize = os.path.getsize(os.path.join(target, file.string))
    time_elapsed = time.time() - start
    print(
        f'Finished downloading "{file.string}" after {round(time_elapsed)} seconds. ({round(filesize/time_elapsed)} bytes per second)')


if __name__ == '__main__':
    sync()
