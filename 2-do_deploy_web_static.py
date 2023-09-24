#!/usr/bin/python3
"""generating .tgz from webstatic and deploy it to server"""
from fabric.api import local, env, run, put, sudo
import os.path


env.hosts = ['100.26.234.25', '100.26.235.62']


def do_deploy(archive_path):
    """Deploy archive to servers"""
    if os.path.isFile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
            format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
            format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
            format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
            format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
            format(name)).failed is True:
        return False
    return True


if __name__ == "__main__":
    do_deploy(archive_path)
