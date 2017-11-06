#!/usr/bin/env python3

import pysftp
import config
import os

def get_remote_filelist(conn) -> list:
    with conn.cd(config.remote_directory):
        return conn.ls()


if __name__ == '__main__':
    pass

