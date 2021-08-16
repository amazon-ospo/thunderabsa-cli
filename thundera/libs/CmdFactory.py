class CmdFactory:

    def __init__(self, targetPath):
        self.targetPath = targetPath
        self.cmdOptions = ["ctags"]

    def setLang(self, langName):
        langStr = "-x -R --fields=+l"
        self.cmdOptions.append(langStr)
        langStr = "--languages="+langName
        self.cmdOptions.append(langStr)

    def setLangMap(self, langMap):
        langStr = "--langmap="+langMap
        self.cmdOptions.append(langStr)

    def setOption(self, cmdOpt):
        self.cmdOptions.append(cmdOpt)

    def buildCmd(self):
        cmdToStr = ' '.join([str(elem) for elem in self.cmdOptions])
        return cmdToStr + ' ' + self.targetPath
