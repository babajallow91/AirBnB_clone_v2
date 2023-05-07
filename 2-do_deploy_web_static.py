#!/usr/bin/python3
"""Distributes an archive to your web servers"""
import os
from fabric.api import *

env.hosts = ['54.165.42.169', '54.175.145.139']


def do_deploy(archive_path):
    """deploys the archive to the servers and updates it"""
    if not os.path.isfile(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Uncompress the archive to the folder
        # /data/web_static/releases/<archive filename without extension>
        # on the web server
        filename = os.path.basename(archive_path)
        folder_name = '/data/web_static/releases/' + filename.split('.')[0]
        run('mkdir -p {}'.format(folder_name))
        run('tar -xzf /tmp/{} -C {}'.format(filename, folder_name))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(filename))

        # Delete the symbolic link /data/web_static/current from the web server
        run('rm -rf /data/web_static/current')

        # Create a new the symbolic link /data/web_static/current on the
        # web server linked to the new version of your code
        # (/data/web_static/releases/<archive filename without extension>)
        run('ln -s {} /data/web_static/current'.format(folder_name))

        return True
    except Exception:
        return False
