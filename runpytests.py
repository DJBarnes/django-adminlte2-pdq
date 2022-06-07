#!/usr/bin/env python
import os
import subprocess
import sys


def runtests():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    os.environ.setdefault('PYTHONPATH', ROOT_DIR)
    argv = ['pytest'] + sys.argv[1:]
    subprocess.run(argv)


if __name__ == '__main__':
    runtests()
