#!/usr/bin/python3
"""deleting out-of-date archives"""
import os
from fabric.api import *


env.hosts = ['100.26.234.25', '100.26.235.62']


def do_clean(number=0):
    """Delete out of date archives
    Args:
        number : number of archives to keep
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(x)) for x in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [x for x in archives if "web_static_" in x]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(x)) for x in archives]
