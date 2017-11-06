#!/usr/bin/env python3

import pysftp
import config2
import os


def get_remote_filelist(conn: pysftp.Connection) -> list:
    return conn.listdir()


def local_file_exists(file):
    pass

def download_file(file)

if __name__ == '__main__':
    with pysftp.Connection(host=config2.ftp_host, username=config2.ftp_user, private_key=config2.ftp_key) as conn:
        with conn.cd(config2.remote_directory):
            files = get_remote_filelist(conn)
            for file in files:
                if not local_file_exists(file):
                    download_file()
