class BinaryCode:

    def convertInstruction(self, instruction, symbolTable):
        return self.getBinaryValue(instruction, symbolTable)

    def getBinaryValue(self, instruction, symbolTable):
        if instruction[0] == '@':
            if instruction[2] == 'symbol':
                symbolValue = symbolTable.getAndSetSymbolValue(instruction[1])
            else:
                symbolValue = instruction[1]
            binaryValue = bin(symbolValue)[2:]
            binaryValue = binaryValue.zfill(16)
        else:
            binaryValue = '111'
            binaryValue += symbolTable.getComputationValue(instruction[1])
            binaryValue += symbolTable.getDestinationValue(instruction[0])
            binaryValue += symbolTable.getJumpValue(instruction[2])

        return binaryValue