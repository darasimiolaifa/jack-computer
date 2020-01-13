from Tokenizer import Tokenizer
from Parser import Parser
import sys
from pathlib import Path


class Program:

    def __init__(self):
        self.jackFile = Path(sys.argv[1])

        # set up file properties
        if self.jackFile.is_file():
            self.fileLists = [self.jackFile]
            self.parent = str(self.jackFile.parent)

        elif self.jackFile.is_dir():
            self.fileLists = [file for file in self.jackFile.iterdir() if str(file).endswith('.jack')]
            self.parent = str(self.jackFile)

    def run(self):
        # process and compile each class
        for file in self.fileLists:
            filename = file.stem
            fileHandle = open(str(file))
            self.tokenizer = Tokenizer()
            self.parser = Parser(self.parent, filename)
            self.compileCode(fileHandle)

        print('Code successfully compiled')

    # tokenize file and compile the tokens
    def compileCode(self, fileHandle):
        tokens = self.tokenizer.tokenize(fileHandle)
        self.parser.parse(tokens)
        fileHandle.close()
        return

if __name__ == "__main__":
    print('Compiling code. Please wait...')
    Program().run()