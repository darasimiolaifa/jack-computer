
class symbolTable:
    symbolTable = dict()
    jumpTable = dict()
    computationTable = dict()
    destinationTable = dict()

    def __init__(self):
        jumpOptions = ['null', 'JGT', 'JEQ', 'JGE', 'JLT', 'JNE', 'JLE', 'JMP']
        destinationOptions = ['null', 'M', 'D', 'MD', 'A', 'AM', 'AD', 'AMD']

        self.populateSymboltable()
        self.populateJumpDestinationTable(self.jumpTable, jumpOptions)
        self.populateJumpDestinationTable(self.destinationTable, destinationOptions)
        self.populateComputationTable()

    def populateSymboltable(self):
        # populate symbol table with reserved registers
        for counter in range(16):
            symbolKey = 'R' + str(counter)
            self.symbolTable[symbolKey] = counter
        self.symbolTable['SCREEN'] = 16384
        self.symbolTable['KBD'] = 24576

        # populate symbol table with other reserved keywords
        otherReservedSymbols = ['SP', 'LCL', 'ARG', 'THIS', 'THAT']
        for integer in range(len(otherReservedSymbols)):
            otherKey = otherReservedSymbols[integer]
            self.symbolTable[otherKey] = integer


    def populateJumpDestinationTable(self, table, options):
        for index in range(len(options)):
            value = bin(index)[2:]
            value = value.zfill(3)
            table[options[index]] = value

    def populateComputationTable(self):
        self.computationTable = {
            '0' : '101010',
            '1' : '111111',
            '-1' : '111010',
            'D' : '001100',
            'A' : '110000',
            '!D' : '001101',
            '!A' : '110001',
            '-D' : '001111',
            '-A' : '110011',
            'D+1' : '011111',
            'A+1' : '110111',
            'D-1' : '001110',
            'A-1' : '110010',
            'D+A' : '000010',
            'D-A' : '010011',
            'A-D' : '000111',
            'D&A' : '000000',
            'D|A' : '010101'
        }


    def getAndSetSymbolValue(self, symbol):
        #get the next available register
        totalSymbols = len(self.symbolTable)
        nextAvailableRegister = totalSymbols - 7

        #get the symbol value or put it in the next available register, if not exist
        self.symbolTable[symbol] = self.symbolTable.get(symbol, nextAvailableRegister)
        return self.symbolTable[symbol]

    def getComputationValue(self, computation):
        index = computation.find('M')
        if index > -1:
            computation = computation[:index] + 'A' + computation[index+1:]
            value = '1' + self.computationTable[computation]
        else:
            value = '0' + self.computationTable[computation]

        return value

    def getDestinationValue(self, destination):
        return self.destinationTable.get(destination, 'err')

    def getJumpValue(self, jump):
        return self.jumpTable.get(jump, 'err')
