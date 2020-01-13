from VMParser import VMParser
from CodeWriter import CodeWriter
import sys
from pathlib import Path


# noinspection PyUnboundLocalVariable
class VMTranslator:

    def __init__(self):
        self.parser = VMParser()
        self.coder = CodeWriter()
        self.myPath = Path(sys.argv[1])
        self.initParameters()

    def initParameters(self):
        self.filelists = list()
        if self.myPath.is_file():
            self.filelists = [self.myPath]
            self.outputFile = str(self.myPath.with_suffix('.asm'))
        elif self.myPath.is_dir():
            self.filelists = [file for file in self.myPath.iterdir() if str(file).endswith('.vm')]
            self.outputFile = str(self.myPath) + ('/' + str(self.myPath.stem) + '.asm')
        self.outputFileHandle = open(self.outputFile, 'w')

    def run(self):
        self.outputFileHandle.write(self.coder.translateCode(['bootstrap'], 'Call Sys.init 0'))

        for file in self.filelists:
            fileHandle = open(str(file))
            filename = file.stem #extract filename without the extendion e.g foo.vm => foo

            self.coder.setFilename(filename)

            for line in fileHandle:
                sanitizedLine = self.sanitizeInput(line)
                if len(sanitizedLine) == 0 : continue
                parsedInstruction = self.parser.parse(sanitizedLine)
                codeString = self.coder.translateCode(parsedInstruction, sanitizedLine)
                self.outputFileHandle.write(codeString)
            fileHandle.close()

        print('Translated VM code to assembly successfully.')
        # noinspection PyUnboundLocalVariable
        self.outputFileHandle.close()

    # remove whitespace and comments from input[line]
    def sanitizeInput(self, line):
        if len(line) == 0 or line.startswith('//'):
            return ''
        line = line.strip()
        commentIndex = line.find('//')
        if commentIndex > -1:
            line = line[:commentIndex]
        return line

if __name__ == "__main__":
    print('Translating VM code to assembly. Please wait...')
    VMTranslator().run()