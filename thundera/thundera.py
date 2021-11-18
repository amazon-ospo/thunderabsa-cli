#!/usr/bin/env python3
import os
import sys
import click
import calendar
import time
import terminal_banner
from shutil import which
from pathlib import Path
from thundera.libs import ErrorHandler
from thundera.libs import FileScanner
from thundera.libs import FolderScanner
from thundera.libs import File


os.environ['LANG'] = 'C.UTF-8'
os.environ['LC_ALL'] = 'C.UTF-8'

debug = ErrorHandler.ErrorHandler(__name__)


@click.command()
@click.argument(
    'target',
    type=click.Path(exists=True)
)
@click.option(
    '-wd',
    '--workdir',
    default=str(calendar.timegm(time.gmtime())),
    help='Working directory'
)
def cli(target, workdir):

    """ Thundera BSA """
    banner_txt = "Thundera Binary Static Analysis (BSA)"
    banner_obj = terminal_banner.Banner(banner_txt)
    print(banner_obj)
    print('')

    cmdlist = ["ctags", "readelf", "exiftool", "strings"]
    for cmd in cmdlist:
        if which(cmd) is None:
            eMSG = "Thundera requires "+cmd+" to run"
            debug.error(eMSG)
            eMSG = "Please install to continue..."
            debug.error(eMSG)
            exit()

    if os.name == "posix":
        if target.endswith('/'):
            target = target[:-1]
        if os.path.isdir(target):
            eMSG = "Scanning the folder "+target
            print(eMSG)
            scanner = FolderScanner.FolderScanner(target)
        elif os.path.isfile(target):
            eMSG = "Scanning the file "+target
            print(eMSG)
            scanner = FileScanner.FileScanner(target)
        else:
            debug.info('*** Target Path: %s' % target)
            debug.info('*** Working Directory: %s' % workdir)
            eMSG = "The target " + target
            eMSG = eMSG + " it\'s a special file (socket, FIFO, device file)"
            debug.error(eMSG)
            print(eMSG)
            print('')
    else:
        eMSG = "Thundera BSA only supports POSIX based OS"
        debug.error(eMSG)
        print(eMSG)
        print('')


if __name__ == '__main__':
    cli()
