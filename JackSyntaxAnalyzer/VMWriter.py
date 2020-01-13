
class VMWriter:

    def __init__(self,directory, filename):
        self.outputFilename = directory + '/' + filename + '.vm'
        self.vmFileHandler = open(self.outputFilename, 'w')

    def writePush(self, segment, index):
        self.vmFileHandler.write('push {0} {1}\n'.format(segment, index))

    def writePop(self, segment, index):
        self.vmFileHandler.write('pop {0} {1}\n'.format(segment, index))

    def writeArithmetic(self, operator):
        self.vmFileHandler.write('{0}\n'.format(operator))

    def writeCall(self, functionName, numberOfArgs):
        self.vmFileHandler.write('call {0} {1}\n'.format(functionName, numberOfArgs))

    def writeFunction(self, functionName, numberOfArgs):
        self.vmFileHandler.write('function {0} {1}\n'.format(functionName, numberOfArgs))

    def writeLabel(self, label):
        self.vmFileHandler.write('label {0}\n'.format(label))

    def writeGOTO(self, label):
        self.vmFileHandler.write('goto {0}\n'.format(label))

    def writeIFGOTO(self, label):
        self.vmFileHandler.write('if-goto {0}\n'.format(label))

    def writeReturn(self):
        self.vmFileHandler.write('return\n')

    def close(self):
        self.vmFileHandler.close()