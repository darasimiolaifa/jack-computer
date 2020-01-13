from Parser import Parser
from symbolTable import symbolTable
from BinaryCode import BinaryCode
import sys
from pathlib import Path


class Program:

    def __init__(self):
        self.parser = Parser()
        self.symbolMap = symbolTable()
        self.binaryConverter = BinaryCode()
        self.filename = Path(sys.argv[1])
        self.outputFile = self.filename.stem + '.hack'
        self.outputFileHandle = open(self.outputFile, "w")

    def run(self):
        # get the list of instructions
        listOfInstructions = self.fillBranchingCode(sys.argv[1])
        
        # interpret list of instructions and write to output file
        for line in listOfInstructions:
            parsedResponse = self.parser.parse(line)
            binaryValue = self.binaryConverter.convertInstruction(parsedResponse, self.symbolMap)
            self.outputFileHandle.write(binaryValue + "\n")
        self.outputFileHandle.close()
        
        print("Code converted to machine language successfully.")


    def sanitizeInput(self, line):
        #check that line isn't empty or just a comment
        if len(line) == 0 or line.startswith("//"):
            return ''
        line = line.strip()
        commentIndex = line.find("//")
        if commentIndex > -1:
            line = line[:commentIndex]
        return line

    def fillBranchingCode(self, file):
        instructionList = list()
        fileHandle = open(file)
        lineCounter = -1

        for line in fileHandle:
            #remove comments from instruction
            cleanLine = self.sanitizeInput(line)
            if len(cleanLine) == 0: continue

            lineCounter += 1
            if cleanLine.startswith('(') and cleanLine.endswith(')'): # resolve lines with branching variables
                variable = cleanLine[1:-1]
                self.symbolMap.symbolTable[variable] = lineCounter
                lineCounter -= 1
            else:
                instructionList.append(cleanLine)   # add valid instruction lines to instruction list
        fileHandle.close()
        return instructionList




if __name__ == '__main__':
    print("Converting to machine code. Please wait...")
    Program().run()