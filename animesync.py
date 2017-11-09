#!/usr/bin/env python3
import time

from termcolor import colored
import config
import pysftp
import sys
import os
import re

# broken, and I also don’t really care about the resolution or crc tag
# filepattern = re.compile(r'(\[(?P<tag>.*)\])?\s?(?P<anime>.*)\s?[-–—]\s?(?P<episode>\d+)\s?([([](?P<resolution>\d{2,5}p?)[)\]])?\s?(\[(?P<crc>[0-9a-fA-F]{6})\])?\.(mkv|mp4)')
filepattern = re.compile(r'(\[(?P<tag>.*)\])?\s?(?P<title>.*?)\s?[-–—]\s?(?P<episode>\d+).*\.(mkv|mp4)')


def sync() -> None:
    try:
        conn = pysftp.Connection(host=config.ftp_host, username=config.ftp_user, private_key=config.ftp_key)
    except Exception as eX:
        if isinstance(eX, FileNotFoundError):
            print(colored('[ERROR]', 'red'), f'Private key at {config.ftp_key} could not be found.')
        elif 'Authentication' in str(type(eX)):
            print(colored('[ERROR]', 'red'), 'Failed to authenticate. Please check your login credentials.')
        else:
            print(colored('[ERROR]', 'red'), 'Could not establish connection')
        sys.exit(-1)
    try:
        conn.chdir(config.remote_directory)
    except FileNotFoundError:
        print(colored('[ERROR]', 'red'), f'Directory "{config.remote_directory}" does not exist on the remote server.')
        sys.exit(-1)
    files = get_remote_filelist(conn)
    if len(files) == 0:
        print(colored('[INFO]', 'magenta'), 'No files in remote directory. Exiting.')
        sys.exit(0)

    print(colored('[INFO]', 'magenta'), 'The following files will be synced:')
    print('    ' + '\n    '.join(files))
    print()

    for file in files:
        parsed = parse_filename(file)
        if not local_file_exists(parsed):
            download_file(conn, parsed)
        else:
            print(colored('[INFO]', 'magenta'), end=' ')
            print(f'"{file}" already exists on local system. Skipping.')
        if config.remove_files_after_download:
            print(colored('[INFO]', 'magenta'), end=' ')
            print(f'Removing "{file}" from remote server')
            conn.remove(file)
        print()
    conn.close()
    print(colored('[SUCCESS]', 'green'), end=' ')
    print(f'All files were synced successfully.')


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
    print(colored('[SUCCESS]', 'green'), end=' ')
    print(
        f'Finished downloading "{file.string}" after {round(time_elapsed)} seconds. ({round(filesize/(time_elapsed*10e5), 2)} MB/s)')


if __name__ == '__main__':
    sync()
