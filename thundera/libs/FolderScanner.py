import os
import time
import mimetypes
import hashlib
import tarfile
import gzip
import csv
import sys
from slugify import slugify
from zipfile import ZipFile
from tabulate import tabulate
from pathlib import Path
from . import File
from . import ArchiveHandler
from . import ErrorHandler


class FolderScanner:

    def __init__(self, rootfolder):

        self.debug = ErrorHandler.ErrorHandler(__name__)
        ts = time.time()

        # Files found during scanner
        self.filelist = []

        # Files to Exclude from ArchiveHandler
        self.exfiles = {}

        # List of folders
        self.folders = {}
        self.symbols = {}

        self.rootfolder = rootfolder
        self.scanFolder(rootfolder, '-')
        self.rfname = slugify(rootfolder)

        self.fresults = []
        self.aresults = []
        self.bsaqueue = []

        self.file_count
        self.lcounter = 0

        for fO in self.filelist:
            # print (fO.filename)
            row = [
                fO.checksum,
                fO.filename,
                fO.filetype,
                fO.isbinary,
                fO.isarchive,
                fO.forceign,
                fO.plang,
                fO.pfile,
                fO.filepath]
            if fO.isbinary and not fO.isarchive and not fO.forceign:
                self.bsaqueue.append(row)
            elif fO.isarchive and not fO.forceign:
                self.aresults.append(row)
            else:
                if not fO.forceign:
                    self.fresults.append(row)

        headers = [
            "Checksum",
            "Filename",
            "MimeType",
            "Binary",
            "Archive",
            "Ignore",
            "Language",
            "Parent",
            "Filepath"]

        with open(self.rfname+'-archive.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for row in self.aresults:
                writer.writerow(row)

        with open(self.rfname+'-files.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for row in self.fresults:
                writer.writerow(row)

        headers = [
            "Checksum",
            "Symbols"]

        rowsym = []
        for key in self.symbols:
            rowsym.append([key, self.symbols[key]])

        with open(self.rfname+'-symbols.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for row in rowsym:
                writer.writerow(row)

        # print(self.symbols)
        # for key in self.symbols:
        #    print(key, '->', self.symbols[key])

        dt = str(round(time.time() - ts, 2))
        self.debug.info('Scan took ' + dt + ' seconds')

    def progress(self, count, total):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write(
            '[%s] %s%s %s\r' % (bar, percents, '%', 'scanning...'))
        sys.stdout.flush()

    def scanFolder(self, rootfolder, pfile):
        if len(pfile.strip()) <= 1:
            eMSG = "* Preparing files to be scanned, please wait..."
            print(eMSG)
            kount = [len(files) for _, _, files in os.walk(rootfolder)]
            self.file_count = kount
            self.file_count = sum(self.file_count)
            print(' ', '>', self.file_count, 'files added to the queue.')
            self.lcounter = 0

        for (dirpath, dirnames, filenames) in os.walk(rootfolder):
            for f in filenames:
                if not Path(os.path.join(dirpath, f)).is_symlink():
                    if len(pfile.strip()) <= 1:
                        self.lcounter += 1
                        self.progress(self.lcounter, self.file_count)
                    fileInfo = File.File(self.debug, dirpath, f, pfile)
                    self.filelist.append(fileInfo)
                    symbols = fileInfo.get_symbols()
                    if len(symbols) >= 1:
                        tmpCSV = symbols[list(symbols.keys())[0]].split(',', 1)
                        self.symbols[tmpCSV[0]] = tmpCSV[1]

            for d in dirnames:
                self.folders[d] = dirpath
        if len(pfile.strip()) <= 1:
            sys.stdout.flush()
            print('')
        for ar in self.filelist:
            if ar.isarchive:
                print(' ', '>', ar.filename)
                archfile = os.path.join(ar.filepath, ar.filename)
                if archfile not in self.exfiles.keys():
                    target = os.path.join(ar.filepath, ar.slugify)
                    self.exfiles[archfile] = target
                    ArchiveHandler.ArchiveHandler(
                        self.debug,
                        ar.filepath,
                        ar.filename,
                        ar.filetype,
                        ar.slugify,
                        ar.checksum
                    )
                    self.scanFolder(target, ar.checksum)
