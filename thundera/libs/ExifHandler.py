import json
import subprocess
import os.path
from os import path


class ExifHandler:

    def __init__(self, target):
        self.target = target
        self.tags = [
            'FileDescription',
            'FileVersion',
            'InternalName',
            'LegalCopyright',
            'OriginalFileName',
            'ProductName',
            'ProductVersion',
            'Comments']
        self.fileMeta = {}

    def run(self):
        if(path.exists(self.target)):
            cmd = "exiftool -json " + self.target
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            (result, error) = process.communicate()
            rc = process.wait()
            process.stdout.close()
            if len(result) >= 2:
                jsonData = json.loads(result.decode('utf-8'))[0]
                for tag in self.tags:
                    try:
                        self.fileMeta[tag] = jsonData[tag]
                    except KeyError:
                        self.fileMeta[tag] = ''
        return self.fileMeta
