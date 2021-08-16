import os
import re
import json
import mimetypes
import hashlib
import magic
import subprocess
from slugify import slugify
from binaryornot.check import is_binary
from . import FileHandler
from . import ExifHandler


class File(object):
    def __init__(self, errorHandler, filepath, filename, pfile):
        self.debug = errorHandler
        self.filepath = filepath
        self.filename = filename
        targetF = os.path.join(filepath, filename)
        self.checksum = self.file_checksum(targetF)
        mime = magic.Magic(mime=True)
        self.filetype = mime.from_file(targetF)
        self.isarchive = self.is_archive(self.filetype)
        self.metadata = self.metadata(
            self.filetype, os.path.join(filepath, filename))
        self.filesize = self.file_size(targetF)
        self.slugify = slugify(filename)
        self.pfile = pfile
        self.isbinary = is_binary(os.path.join(filepath, filename))
        self.forceign = self.check_ignore(self.filetype, filepath, filename)
        self.plang = 'none'
        self.symstat = 0
        self.csv = {}
        if not self.isarchive and not self.forceign:
            fCSV = os.path.splitext(filename)[0]
            fileHandler = FileHandler.FileHandler(
                self.debug,
                filepath,
                filename,
                self.filetype,
                self.checksum)
            self.csv[fCSV] = fileHandler.run_handler()

    def get_symbols(self):
        rCSV = {}
        for key, value in self.csv.items():
            if value:
                rCSV[key] = value
                self.symstat = len(value)
        return rCSV

    @classmethod
    def new_to_dict(cls, filepath, filename):
        self.checksum = self.file_checksum(os.path.join(filepath, filename))
        dictionary[checksum] = cls(filepath, filename)

    def convert_bytes(self, num):
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0

    def check_ignore(self, file_type, filepath, filename):
        list_mimes = [
            'application/x-git',
            'text/plain'
            ]
        list_subfolders = [
            '.git'
            ]
        if file_type in list_mimes:
            return True
        else:
            for sf in list_subfolders:
                if sf in filepath:
                    return True
                else:
                    return False

    def is_archive(self, file_type):
        # This function needs to be replaced by the info from ArchiveHandler
        list_mimes = [
            'application/java-archive',
            'application/zip',
            'application/java-archive',
            'application/gzip',
            'application/zlib',
            'application/x-tar'
            ]
        if file_type in list_mimes:
            return True
        else:
            return False

    def metadata(self, file_type, file_path):
        # This function needs to be replaced by the info from ArchiveHandler
        list_mimes = [
            'application/x-dosexec',
            'application/x-sharedlib',
            'font/sfnt'
            ]
        if file_type in list_mimes:
            exif = ExifHandler.ExifHandler(file_path)
            return exif.run()
        else:
            return ''

    def file_size(self, file_path):
        if os.path.isfile(file_path):
            file_info = os.stat(file_path)
            return self.convert_bytes(file_info.st_size)

    def file_checksum(self, file_path):
        with open(file_path, "rb") as f:
            file_hash = hashlib.md5()
            chunk = f.read(8192)
            while chunk:
                file_hash.update(chunk)
                chunk = f.read(8192)
        return file_hash.hexdigest()
