import subprocess
from . import CmdFactory


class CtagsHandler:

    def __init__(self, target):
        self.target = target
        self.cmd = CmdFactory.CmdFactory(target)
        self.symlst = []

    def setLang(self, langName):
        self.cmd.setLang(langName)

    def setLangMap(self, langMap):
        self.cmd.setLangMap(langMap)

    def setOption(self, cmdOpt):
        self.cmd.setOption(cmdOpt)

    def run(self):
        cmd = self.cmd.buildCmd()
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        (result, error) = process.communicate()
        rc = process.wait()
        process.stdout.close()
        for line in result.decode('utf-8').splitlines():
            cols = line.split()
            if len(cols) >= 2:
                if len(cols[0]) >= 5:
                    self.symlst.append(cols[0])
        self.symlst = sorted(set(self.symlst))
        return ','.join(self.symlst)
