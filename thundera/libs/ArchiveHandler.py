import os
import mimetypes
import hashlib
import tarfile
import gzip
import zlib
import pprint
from zipfile import ZipFile
from . import File


class ArchiveHandler:

    def __init__(self, eH, filepath, filename, filetype, slugify, checksum):
        self.debug = eH
        self.filepath = filepath
        self.filename = filename
        self.filetype = filetype
        self.slugify = slugify
        self.checksum = checksum
        self.archive_handler(filepath, filename, filetype, slugify, checksum)

    def preload_handlers(self):
        return {
            'application/zip': self.unzip_archive,
            'application/java-archive': self.unzip_archive,
            'application/gzip': self.ungzip_archive,
            'application/zlib': self.unzlib_archive,
            'application/tar': self.untar_archive,
            'application/x-tar': self.untar_archive
        }

    def archive_handler(self, filepath, filename, filetype, slugify, checksum):
        # Pending recursive extraction
        try:
            handlers = self.preload_handlers()
            handler = handlers[filetype]
            source = os.path.join(filepath, filename)
            target = os.path.join(filepath, slugify)
            self.debug.info('handling ' + filetype)
            handler(filepath, filename, slugify)
        except KeyError:
            self.debug.error('handler not implemented for ' + filetype)

    def unzlib_archive(self, filepath, filename, slugify):
        f = open(os.path.join(filepath, filename), 'rb').read()
        df = os.path.splitext(filename)[0]+'.dmp'
        tf = os.path.join(filepath, df)
        f_out = open(tf, 'wb')
        f_out.write(zlib.decompress(f))
        f_out.close()

    def ungzip_archive(self, filepath, filename, slugify):
        if filename.endswith("tgz"):
            self.untar_archive(filepath, filename, slugify)
        elif filename.endswith("tar.gz"):
            self.untar_archive(filepath, filename, slugify)
        else:
            print('gzip')
            f = gzip.open(os.path.join(filepath, filename), 'r')
            file_content = f.read()
            file_content = file_content.decode('utf-8')
            nm = os.path.splitext(filename)[0]
            tf = os.path.join(filepath, nm)
            f_out = open(tf, 'w+')
            f_out.write(file_content)
            f.close()
            f_out.close()

    def unzip_archive(self, filepath, filename, slugify):
        with ZipFile(os.path.join(filepath, filename), 'r') as zipObj:
            zipObj.extractall(os.path.join(filepath, slugify))

    def untar_archive(self, filepath, filename, slugify):
        if filename.endswith("tar.gz"):
            TarFile = tarfile.open(os.path.join(filepath, filename), "r:gz")
            TarFile.extractall(os.path.join(filepath, slugify))
            TarFile.close()
        elif filename.endswith("tgz"):
            TarFile = tarfile.open(os.path.join(filepath, filename), "r:gz")
            TarFile.extractall(os.path.join(filepath, slugify))
            TarFile.close()
        elif filename.endswith("tar"):
            TarFile = tarfile.open(os.path.join(filepath, filename), "r:")
            TarFile.extractall(os.path.join(filepath, slugify))
            TarFile.close()
