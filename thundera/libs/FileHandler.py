import os
import lief
import re
import mimetypes
import hashlib
import os.path
import subprocess
from os import path
from string import digits
from . import CtagsHandler

class FileHandler:

    def __init__(self, errorHandler, filepath, filename, filetype, checksum):
        self.debug = errorHandler
        self.filepath = filepath
        self.filename = filename
        self.filetype = filetype
        self.checksum = checksum

    def preload_handlers(self):
        # This should be replaced by a BD
        return {
            'text/x-c': self.handle_cplusplus,
            'text/x-c++': self.handle_cplusplus,
            'text/x-python': self.handle_python,
            'text/x-perl': self.handle_perl,
            'text/x-ruby': self.handle_ruby,
            'text/x-rust': self.handle_rust,
            'text/x-java': self.handle_java,
            'text/x-objective-c': self.handle_objectivec,
            'application/x-mach-binary': self.handle_mach_o,
            'application/x-sharedlib': self.handle_sharedlib,
            'application/x-dosexec': self.handle_strings,
            'font/sfnt': self.handle_strings,

            'application/octet-stream': self.ignore,
            'application/x-ms-pdb': self.ignore,
            'image/vnd.microsoft.icon': self.ignore,
            'text/x-shellscript': self.ignore,
            'text/xml': self.ignore,
            'application/csv': self.ignore,
            'text/x-tex': self.ignore,
            'text/x-makefile': self.ignore,
            'application/json': self.ignore,
            'text/html': self.ignore,
            'image/x-portable-pixmap': self.ignore,
            'image/webp': self.ignore,
            'image/png': self.ignore,
            'image/x-tga': self.ignore,
            'image/g3fax': self.ignore,
            'image/gif': self.ignore,
            'image/jpeg': self.ignore,
            'application/x-wine-extension-ini': self.ignore,
            'audio/mpeg': self.ignore,
            'audio/x-wav': self.ignore,
            'video/mp4': self.ignore,
            'inode/x-empty': self.ignore
        }

    def run_handler(self):
        try:
            handlers = self.preload_handlers()
            handler = handlers[self.filetype]
            return handler(self.filepath, self.filename, self.checksum)
        except KeyError:
            self.debug.error('handler not implemented for ' + self.filetype)
            fullPath = os.path.join(self.filepath, self.filename)
            self.debug.error('skipping ' + fullPath)

    def ignore(self, filepath, filename, checksum):
        self.debug.info('skipping ' + self.filename)
        return ''

    def handle_strings(self, filepath, filename, checksum):
        fullpath = filepath+"/"+filename
        if(path.exists(fullpath)):
            cmd = 'strings -n 5 ' + fullpath
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            (result, error) = process.communicate()
            rc = process.wait()
            process.stdout.close()
            rstTXT = result.decode('utf-8')
            results = self.stripNonAlphaNum(' '.join(rstTXT.split()))
            prow = checksum + ",".join(results)
            prow = prow + "," + os.path.splitext(filename)[0]
            return prow

    def handle_sharedlib(self, filepath, filename, checksum):
        fullPath = os.path.join(filepath, filename)
        libSO = lief.parse(fullPath)
        symbols = []
        iter = filter(lambda e: e.exported, libSO.dynamic_symbols)
        for idx, lsym in enumerate(iter):
            symbols.extend(self.demangle(lsym.name))
        symbols = list(set(symbols))
        prow = checksum + ','
        prow = prow + ",".join(symbols)
        prow = prow + "," + os.path.splitext(filename)[0]
        return prow

    def handle_mach_o(self, filepath, filename, checksum):
        fullPath = os.path.join(filepath, filename)
        libSO = lief.parse(fullPath)
        symbols = []
        #for c in libSO.commands:
        #    if c.command.name in ["LOAD_DYLIB", "LOAD_WEAK_DYLIB"]:
        #        print("{:20} {}".format(
        #            c.command.name,
        #            c.name
        #        ))
        remove_digits = str.maketrans(',', ',', digits)
        for i in libSO.symbols:
            symbol = i.name
            symbol = re.sub("[^a-zA-Z0-9]+", ",", symbol)
            symbol = re.sub("\d+", ",", symbol)
            symbols.extend(symbol.split(','))
        symbols = list(set(symbols))
        while("" in symbols):
            symbols.remove("")
        prow = checksum + ','
        prow = prow + ",".join(symbols)
        prow = prow + "," + os.path.splitext(filename)[0]
        return prow

    def handle_objectivec(self, filepath, filename, checksum):
        fname = os.path.splitext(filename)[0]
        target = os.path.join(filepath, filename)
        ctags = CtagsHandler.CtagsHandler(target)
        ctags.setLang('objectivec')
        ctags.setLangMap('objectivec:.h.m')
        rst = ','.join([checksum, ctags.run(), fname])
        return rst

    def handle_rust(self, filepath, filename, checksum):
        fname = os.path.splitext(filename)[0]
        target = os.path.join(filepath, filename)
        ctags = CtagsHandler.CtagsHandler(target)
        ctags.setLang('Rust')
        ctags.setLangMap('Rust:.rs')
        rst = ','.join([checksum, ctags.run(), fname])
        return rst

    def handle_ruby(self, filepath, filename, checksum):
        fname = os.path.splitext(filename)[0]
        target = os.path.join(filepath, filename)
        ctags = CtagsHandler.CtagsHandler(target)
        ctags.setLang('ruby')
        ctags.setLangMap('ruby:+.rake')
        rst = ','.join([checksum, ctags.run(), fname])
        return rst

    def handle_perl(self, filepath, filename, checksum):
        fname = os.path.splitext(filename)[0]
        target = os.path.join(filepath, filename)
        ctags = CtagsHandler.CtagsHandler(target)
        ctags.setLang('Perl')
        ctags.setLangMap('Perl:+.t')
        rst = ','.join([checksum, ctags.run(), fname])
        return rst

    def handle_cplusplus(self, filepath, filename, checksum):
        fname = os.path.splitext(filename)[0]
        target = os.path.join(filepath, filename)
        ctags = CtagsHandler.CtagsHandler(target)
        ctags.setOption('--kinds-C++=+l')
        ctags.setOption('-o -')
        rst = ','.join([checksum, ctags.run(), fname])
        return rst

    def handle_python(self, filepath, filename, checksum):
        fname = os.path.splitext(filename)[0]
        target = os.path.join(filepath, filename)
        ctags = CtagsHandler.CtagsHandler(target)
        ctags.setLang('python')
        ctags.setOption('--python-kinds=-iv')
        rst = ','.join([checksum, ctags.run(), fname])
        return rst

    def handle_java(self, filepath, filename, checksum):
        fname = os.path.splitext(filename)[0]
        target = os.path.join(filepath, filename)
        ctags = CtagsHandler.CtagsHandler(target)
        ctags.setLang('Java')
        ctags.setLangMap('java:+.aj')
        rst = ','.join([checksum, ctags.run(), fname])
        return rst

    def stripNonAlphaNum(self, text):
        return re.compile(r'\W+', re.UNICODE).split(text)

    def demangle(self, name):
        cmd = 'c++filt ' + name
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        (result, error) = process.communicate()
        rc = process.wait()
        process.stdout.close()

        results = self.stripNonAlphaNum(result.decode('utf-8'))
        return ' '.join(results).split()
