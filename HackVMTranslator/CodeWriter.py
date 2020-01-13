import random
import string

class CodeWriter:

    def __init__(self):
        self.initializeSymbols()

    # used to set the current filename for several parts of the code that need it
    def setFilename(self, filename):
        self.filename = filename

    # runs the whole translation code based on the input from the main class
    def translateCode(self, codeInstruction, unparsedCodeInstruction):
        instruction = codeInstruction[0]
        translatedCommand = ''
        commandComment = '//{0}\n'.format(unparsedCodeInstruction) # comment for each block of translation in assembly

        # translation block
        if instruction in self.binaryALCommands:
            translatedCommand = self.translateBinaryALCommands(self.binaryALCommands[instruction])
        elif instruction in self.unaryALCommands:
            translatedCommand = self.translateUnaryALCommands(self.unaryALCommands[instruction])
        elif instruction in self.comparisonALCommands:
            translatedCommand = self.translateComparisonALCommands(self.comparisonALCommands[instruction])
        elif instruction in self.memoryAccessCommands:
            translatedCommand = self.translateMACommands(codeInstruction)
        elif instruction == 'label':
            translatedCommand = self.translateLabelCommands(codeInstruction[1])
        elif instruction == 'goto':
            translatedCommand = self.translateGOTOCommands(codeInstruction[1])
        elif instruction == 'if-goto':
            translatedCommand = self.translateIfGOTOCommands(codeInstruction[1])
        elif instruction == 'call':
            translatedCommand = self.translateCallCommands(codeInstruction[1], codeInstruction[2], self.filename)
        elif instruction == 'function':
            translatedCommand = self.translateFunctionCommands(codeInstruction[1], codeInstruction[2])
        elif instruction == 'return':
            translatedCommand = self.translateReturnCommands('function')
        elif instruction == 'bootstrap':
            translatedCommand = self.bootstrapCode()

        finalOutput = commandComment + translatedCommand.replace(' ', '\n') + '\n'
        return finalOutput

    # used to initialize the major code differences of each arithmetic/logical command, and the memory address lists
    def initializeSymbols(self):
        self.binaryALCommands = {
            'add' : 'M=D+M',
            'sub' : 'M=M-D',
            'and' : 'M=D&M',
            'or' : 'M=D|M'
        }
        self.comparisonALCommands = {
            'eq': 'JEQ',
            'lt': 'JLT',
            'gt': 'JGT'
        }
        self.unaryALCommands = {
            'neg': 'M=-M',
            'not': 'M=!M'
        }

        self.dynamicAddress = {'local' : 'LCL', 'argument' : 'ARG', 'this' : 'THIS', 'that' : 'THAT'}
        self.memoryAccessCommands = ['push', 'pop']
        self.returnLevels = 1
        self.labelCounter = 0

    # translates commands like ADD, SUB, AND etc
    def translateBinaryALCommands(self, line):
        instructionString = '@SP A=M-1 D=M A=A-1 {0} D=A @SP M=D+1 '.format(line)
        return instructionString

    # translates the commands NOT and NEG
    def translateUnaryALCommands(self, line):
        instructionString = '@SP A=M-1 {0} '.format(line)
        return instructionString

    def advanceLabelCounter(self):
        self.labelCounter += 1
        return self.labelCounter

    # translates the commands EQ, GT, and LT
    def translateComparisonALCommands(self, line):
        #rand = ''.join([random.choice(string.digits) for x in range(4)])
        label1 = self.advanceLabelCounter()
        label2 = self.advanceLabelCounter()
        instructionString = '@SP A=M-1 D=M A=A-1 D=M-D M=0 @label L{0} D;{2} @label L{1}\
         0;JMP (label L{0}) @2 D=A @SP A=M-D M=-1 (label L{1}) @SP M=M-1 '.format(label1, label2, line)
        return instructionString

    # translates the memory access commands PUSH and POP for all memory segments
    def translateMACommands(self, line):
        if line[0] == 'pop':
            return self.popSegment(line[1:])
        elif line[0] == 'push':
            return self.pushSegment(line[1:])

    def popSegment(self, line):
        instructionString = self.computePopAddress(line[0], line[1])
        instructionString = '{0} M=D @SP M=M-1 '.format(instructionString)
        return instructionString

    def pushSegment(self, line):
        instructionString = self.computePushAddress(line[0], line[1])
        instructionString = '{0} {1} '.format(instructionString, self.pushSuffix())
        return instructionString

    # responsible for pushing the just computed value to the stack and advancing the pointer
    def pushSuffix(self):
        return '@SP A=M M=D @SP M=M+1'

    # used to write the initial differences between each memory segment access code
    def computePushAddress(self, address, i):
        prefix = '@{0} D=A'.format(i)
        suffix = 'D=M'
        computedAddress = ''

        if address in self.dynamicAddress:
            computedAddress = '{0} @{1} A=D+M {2}'.format(prefix, self.dynamicAddress[address], suffix)
        elif address == 'constant':
            computedAddress = '{0}'.format(prefix)
        elif address == 'static':
            computedAddress = '@{0}.{1} {2}'.format(self.filename, i, suffix)
        elif address == 'temp':
            computedAddress = '{0} @5 A=D+A {1}'.format(prefix, suffix)
        elif address == 'pointer':
            if i == '0':
                computedAddress = '@THIS {0}'.format(suffix)
            elif i == '1':
                computedAddress = '@THAT {0}'.format(suffix)

        return computedAddress

    def computePopAddress(self, address, i):

        computedAddress = ''
        if address in self.dynamicAddress:
            computedAddress = '@{0} D=A @{1} D=D+M @addr M=D @SP A=M-1 D=M @addr A=M'.format(i, self.dynamicAddress[address])
        elif address == 'static':
            computedAddress = '@SP A=M-1 D=M @{0}.{1}'.format(self.filename, i)
        elif address == 'temp':
            computedAddress = '@{0} D=A @5 D=D+A @addr M=D @SP A=M-1 D=M @addr A=M'.format(i)
        elif address == 'pointer':
            computedAddress = '@SP A=M-1 D=M'
            if i == '0':
                computedAddress += ' @THIS'
            elif i == '1':
                computedAddress += ' @THAT'

        return computedAddress

    # translate label commands
    def translateLabelCommands(self, label):
        return '({0}) '.format(label)

    # translate GOTO commands
    def translateGOTOCommands(self, label):
        return '@{0} 0;JMP '.format(label)

    # translate conditional GOTO commands
    def translateIfGOTOCommands(self, label):
        return '@SP A=M-1 D=M @SP M=M-1 @{0} D;JNE '.format(label)

    # translate call commands
    def translateCallCommands(self, functionName, numberOfArgs, filename):
        # push the return address (the 'line number' of the next instruction at this point) to the stack
        returnAddress = '{0}$ret.{1}'.format(filename, self.returnLevels)
        translation = '@{0} D=A {1} '.format(returnAddress, self.pushSuffix())

        # push the current status of LCL, ARG, THIS, and THAT to the stack
        for index in range(4):
            translation += '@{0} D=M {1} '.format(index + 1, self.pushSuffix())

        # reposition ARG and set LCL to the current value of SP to prepare for the calee
        translation += '@5 D=A @{0} D=D+A @SP D=M-D @ARG M=D @SP D=M @LCL M=D {1} '.format(numberOfArgs, self.translateGOTOCommands(functionName))

        # insert the return address generated and pushed to the stack above
        translation += '({0})'.format(returnAddress)

        self.returnLevels += 1
        return translation

    # translate function commands
    def translateFunctionCommands(self, functionName, numberOfVars):
        translation = '({0}) '.format(functionName)

        # push as many zeros as the local variables of the function to the stack
        translation += self.pushSegment(['constant', '0']) * int(numberOfVars)
        return translation

    # translate return commands
    def translateReturnCommands(self, functionName):
        # create endframe and returnadress variables
        returnAddress = '{0}$returnAddress.{1}'.format(functionName, self.returnLevels)
        endFrame = '{0}$endFrame{1}'.format(functionName, self.returnLevels)

        # fill the variables with the appopriate values from the memory (endframe=LCL; returnaddress=endframe-5)
        translation = '@LCL D=M @{0} M=D @5 A=D-A D=M @{1} M=D '.format(endFrame, returnAddress)

        # put the return value at the position M[ARG] and reset the SP to the next address in memory
        translation += self.popSegment(['argument', '0'])
        translation += '@ARG D=M+1 @SP M=D '

        # restore the previously pushed values of THAT, THIS, ARG and LCL
        for index in range(4):
            translation += '@{0} D=A @{1} A=M-D D=M @{2} M=D '.format(index + 1, endFrame, 4 - index)

        # retrive the returnaddres and jump to it
        translation += '@{0} A=M 0;JMP '.format(returnAddress)
        return translation

    # insert the bootstrap code for initializing the VM
    def bootstrapCode(self):
        return '@256 D=A @SP M=D {0}'.format(self.translateCallCommands('Sys.init', '0', 'Sys'))
