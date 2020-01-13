class Parser:
    instruction = ''

    def __init__(self):
        pass

    def parse(self, string):
        self.instruction = string.strip()
        if self.instruction[0] == '@':
            parsedResponse = self.parseAInstruction(self.instruction)
        else:
            parsedResponse = self.parseCInstruction(self.instruction)
        return parsedResponse

    def parseAInstruction(self, aInstruction):
        if aInstruction[1:].isnumeric():
            response = ["@", int(aInstruction[1:]), None]
        else:
            response = ['@', aInstruction[1:], "symbol"]
        return response

    def parseCInstruction(self, cInstruction):
        if '=' in cInstruction:
            instructionTuple = cInstruction.partition('=')
            destination = instructionTuple[0]
            secondPartition = instructionTuple[2]
        else:
            destination = 'null'
            secondPartition = cInstruction

        if ';' in secondPartition:
            computationAndJump = secondPartition.partition(';')
            computation = computationAndJump[0]
            jump = computationAndJump[2]
        else:
            computation = secondPartition
            jump = 'null'

        response = [destination, computation, jump]
        return response