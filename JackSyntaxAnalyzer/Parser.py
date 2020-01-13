from SymbolTable import SymbolTable
from VMWriter import VMWriter
class Parser:

    def __init__(self, directory, filename):
        self.symbolTable = SymbolTable()
        self.VMWriter = VMWriter(directory, filename)
        self.className = ''

        self.tokens = []
        self.tokenIndex = 0
        self.labelCounter = 0

        self.statementOptions = ['let', 'while', 'do', 'if', 'return']
        self.expressionOptions = ['integerConstant', 'stringConstant', 'identifier']

        self.op = {'+' : 'add', '-' : 'sub', '*' : 'call Math.multiply 2', '/' : 'call Math.divide 2',
                   '=' : 'eq', '<' : 'lt', '>' : 'gt', '&' : 'and', '|': 'or' }
        self.unaryOp = {'-' : 'neg', '~' : 'not'}
        self.keywordConstant = {'true' : 'constant 1\n neg', 'false' : 'constant 0', 'this': 'pointer 0', 'null' : 'constant 0'}

        self.classVariableKinds = ['field', 'static']
        self.subroutineVariableKinds = ['local', 'argument']
        self.subroutineTypes = ['method', 'constructor', 'function']
        self.variableTypes = ['int', 'char', 'boolean']


    def parse(self, tokens):
        self.tokens = tokens
        self.compileClass()
        self.VMWriter.close()
        return


    def expect(self, *args):
        expectedString = self.currentToken()

        if expectedString['value'] not in args and expectedString['type'] != 'identifier':
            print(self.currentToken())
            raise Exception("Expecting either of '{0}'; saw '{1}'".format(','.join([x for x in args]), expectedString['value']))
        else:
            # ateprint(self.currentToken())
            tokenValue = self.currentToken()['value']
            self.advanceIndex(1)
            return tokenValue


    def advanceIndex(self, step):
        self.tokenIndex += step

    def currentToken(self):
        return self.tokens[self.tokenIndex]

    # starts program compilation at class-level
    def compileClass(self):
        self.expect('class')
        self.className = self.compileClassName()
        self.expect('{')

        while self.currentToken()['value'] in self.classVariableKinds:
            self.compileClassVarDec()

        currentToken = self.currentToken()['value']
        while currentToken in self.subroutineTypes:
            self.compileSubroutineDec()
            currentToken = self.currentToken()['value']

        self.expect('}')


    def compileClassVarDec(self):
        variable = dict()
        variable['kind'] = self.expect('static', 'field')
        variable ['type'] = self.compileType()
        variable['name'] = self.compileVarName()
        self.symbolTable.addVariable(variable)

        while self.currentToken()['value'] == ',':
            self.expect(',')
            variable['name'] = self.compileVarName()
            self.symbolTable.addVariable(variable)

        self.expect(';')

    def compileClassName(self):
        return self.expect('')


    def compileSubroutineDec(self):
        # reset the subroutine symbol table for new subroutine
        self.symbolTable.startNewSubroutine()

        self.subroutineType = self.expect('method', 'constructor', 'function')
        if self.subroutineType == 'method':
            # print(self.subroutineType)
            variable = dict()
            variable['kind'] = 'argument'
            variable['type'] = self.className
            variable['name'] = 'this'
            self.symbolTable.addVariable(variable)

        self.returnType = self.expect('void', 'int', 'char', 'boolean')
        self.compileSubroutineName()

        # subroutine name in VM => className.subroutineName
        subroutineName = self.className + '.' + self.subroutineName
        self.expect('(')
        numberOfParameters = self.compileParameterList()
        self.expect(')')
        self.compileSubroutineBody(numberOfParameters, subroutineName)


    def compileSubroutineName(self):
        self.subroutineName = self.expect('')

    def compileParameterList(self):
        numberOfParameters = 0

        if self.currentToken()['type'] == 'identifier' or self.currentToken()['value'] in self.variableTypes:
            numberOfParameters = self.variableList('argument')

        return numberOfParameters


    def compileSubroutineBody(self, numberOfParameters, subroutineName):
        self.expect('{')

        while self.currentToken()['value'] == 'var':
            self.compileVarDec()

        numberOfLocalVars = self.symbolTable.getNumberOfLocalVars()
        self.VMWriter.writeFunction(subroutineName, numberOfLocalVars)

        if self.subroutineType == 'constructor':
            # allocate memory for the instance variables of the  object to be constructed
            memorySpaceNeeded = self.symbolTable.getNumberOfFieldVars()
            self.VMWriter.writePush('constant', memorySpaceNeeded)
            self.VMWriter.writeCall('Memory.alloc', 1)
            # set the base of the THIS segment to the value of the address returned by the Memory.alloc function
            self.VMWriter.writePop('pointer', 0)
        # add the reference to the calling object as argument 0 of the subroutine
        if self.subroutineType == 'method':
            self.VMWriter.writePush('argument', 0)
            self.VMWriter.writePop('pointer', 0)

        #print(subroutineName, self.symbolTable.subroutineSymbolTable)
        self.compileStatements()
        self.expect('}')


    def compileVarDec(self):
        self.expect('var')
        self.variableList('local')
        self.expect(';')


    def variableList(self, kind):
        numberOfParameters = 0

        # populate the respective (calling function) symbol table with the variables found
        variable = dict()
        variable['kind'] = kind
        variable['type'], variable['name'] = self.VarDec()
        self.symbolTable.addVariable(variable)
        numberOfParameters += 1

        # compile multiple variable declarations
        while self.currentToken()['value'] == ',':
            self.expect(',')
            if self.currentToken()['type'] == 'keyword':
                variable['type'] = self.compileType()
            variable['name'] = self.compileVarName()
            self.symbolTable.addVariable(variable)
            numberOfParameters += 1

        return numberOfParameters


    def VarDec(self):
        return self.compileType(), self.compileVarName()

    def compileVarName(self):
        return self.expect('')

    def compileType(self):
        return self.expect('int', 'char', 'boolean')

    def compileStatements(self):
        while self.currentToken()['value'] in self.statementOptions:
            self.compileStatement()

    def compileStatement(self):
        if self.currentToken()['value'] == 'if':
            self.compileIfStatement()
        elif self.currentToken()['value'] == 'while':
            self.compileWhileStatement()
        elif self.currentToken()['value'] == 'let':
            self.compileLetStatement()
        elif self.currentToken()['value'] == 'do':
            self.compileDoStatement()
        elif self.currentToken()['value'] == 'return':
            self.compileReturnStatement()

    def compileIfStatement(self):
        self.expect('if')
        self.expect('(')
        self.compileExpression()
        self.expect(')')
        self.VMWriter.writeArithmetic('not')
        label1 = self.advanceLabelCounter()
        self.VMWriter.writeIFGOTO('L{0}'.format(label1))
        self.expect('{')
        self.compileStatements()
        self.expect('}')
        label2 = self.advanceLabelCounter()
        self.VMWriter.writeGOTO('L{0}'.format(label2))
        self.VMWriter.writeLabel('L{0}'.format(label1))
        if self.currentToken()['value'] == 'else':
            self.expect('else')
            self.expect('{')
            self.compileStatements()
            self.expect('}')
        self.VMWriter.writeLabel('L{0}'.format(label2))

    def advanceLabelCounter(self):
        self.labelCounter += 1
        return self.labelCounter

    def compileWhileStatement(self):
        self.expect('while')
        self.expect('(')
        label1 = self.advanceLabelCounter()
        self.VMWriter.writeLabel('L{0}'.format(label1))
        self.compileExpression()
        self.VMWriter.writeArithmetic('not')
        label2 = self.advanceLabelCounter()
        self.VMWriter.writeIFGOTO('L{0}'.format(label2))
        self.expect(')')
        self.expect('{')
        self.compileStatements()
        self.VMWriter.writeGOTO('L{0}'.format(label1))
        self.expect('}')
        self.VMWriter.writeLabel('L{0}'.format(label2))

    def compileDoStatement(self):
        self.expect('do')
        self.advanceIndex(1)
        self.compileSubroutineCall()
        self.expect(';')
        self.VMWriter.writePop('temp', 0)

    def compileLetStatement(self):
        self.expect('let')
        variable = self.compileVarName()
        segment = self.symbolTable.getVariableKind(variable)
        index = self.symbolTable.getVariablePosition(variable)

        currentToken = self.currentToken()['value']

        if currentToken == '[':
            self.VMWriter.writePush(segment, index)
            self.expect('[')
            self.compileExpression()
            self.expect(']')
            self.VMWriter.writeArithmetic('add')

        self.expect('=')
        self.compileExpression()
        self.expect(';')

        if currentToken == '[':
            self.VMWriter.writePop('temp', 0)
            self.VMWriter.writePop('pointer', 1)
            self.VMWriter.writePush('temp', 0)
            self.VMWriter.writePop('that', 0)
        else:
            self.VMWriter.writePop(segment, index)

    def compileReturnStatement(self):
        self.expect('return')
        currentToken = self.currentToken()
        if currentToken['type'] in self.expressionOptions or currentToken['value'] in self.keywordConstant\
                or self.currentToken()['value'] in self.unaryOp:
            self.compileExpression()
        self.expect(';')
        if self.returnType == 'void':
            self.VMWriter.writePush('constant', 0)
        self.VMWriter.writeReturn()

    def compileSubroutineCall(self):
        subroutineFullName = ''
        numberOfArgs = 0
        if self.currentToken()['value'] == '.':
            self.advanceIndex(-1)
            subroutineFullName = self.compileVarName()
            varType = self.symbolTable.getVariableType(subroutineFullName)
            segment = self.symbolTable.getVariableKind(subroutineFullName)
            index = self.symbolTable.getVariablePosition(subroutineFullName)
            if varType is not None:
                self.VMWriter.writePush(segment, index)
                subroutineFullName = varType
                numberOfArgs += 1
            subroutineFullName += self.expect('.')
            subroutineName, nArgs = self.subroutineCall()
            subroutineFullName += subroutineName
        else:
            self.advanceIndex(-1)
            subroutineName, nArgs = self.subroutineCall()
            subroutineFullName += subroutineName
        numberOfArgs += nArgs
        self.VMWriter.writeCall(subroutineFullName, numberOfArgs)

    def subroutineCall(self):
        subroutineName = self.expect('')
        self.expect('(')
        numberOfArgs = self.compileExpressionList()
        self.expect(')')
        return subroutineName, numberOfArgs

    def compileExpression(self):
        self.compileTerm()
        while self.currentToken()['value'] in self.op.keys():
            operator = self.expect(self.currentToken()['value'])
            self.compileTerm()
            self.VMWriter.writeArithmetic(self.op[operator])

    def compileExpressionList(self):
        numberOfArgs = 0
        currentToken = self.currentToken()
        if currentToken['type'] in self.expressionOptions or currentToken['value'] in self.keywordConstant\
                or currentToken['value'] == '(' or self.currentToken()['value'] in self.unaryOp:
            self.compileExpression()
            numberOfArgs += 1
            while self.currentToken()['value'] == ',':
                self.expect(',')
                self.compileExpression()
                numberOfArgs += 1
        return numberOfArgs

    def compileTerm(self):
        if self.currentToken()['value'] in self.unaryOp.keys():
            operator = self.expect(self.currentToken()['value'])
            self.compileTerm()
            self.VMWriter.writeArithmetic(self.unaryOp[operator])

        elif self.currentToken()['type'] == 'identifier':
            variable = self.currentToken()['value']
            self.advanceIndex(1)
            if self.currentToken()['value'] == '(' or self.currentToken()['value'] == '.':
                self.compileSubroutineCall()

            elif self.currentToken()['value'] == '[':
                segment = self.symbolTable.getVariableKind(variable)
                index = self.symbolTable.getVariablePosition(variable)
                self.VMWriter.writePush(segment, index)
                self.expect('[')
                self.compileExpression()
                self.expect(']')
                self.VMWriter.writeArithmetic('add')
                self.VMWriter.writePop('pointer', 1)
                self.VMWriter.writePush('that', 0)

            else:
                self.advanceIndex(-1)
                variable = self.expect('')
                segment = self.symbolTable.getVariableKind(variable)
                index = self.symbolTable.getVariablePosition(variable)
                self.VMWriter.writePush(segment, index)

        elif self.currentToken()['type'] == 'integerConstant':
            integer = self.expect(self.currentToken()['value'])
            self.VMWriter.writePush('constant', integer)

        elif self.currentToken()['type'] == 'stringConstant':
            string = self.expect(self.currentToken()['value'])
            self.VMWriter.writePush('constant', len(string))
            self.VMWriter.writeCall('String.new', 1)
            for character in string:
                self.VMWriter.writePush('constant', ord(character))
                self.VMWriter.writeCall('String.appendChar', 2)

        elif self.currentToken()['value'] in self.keywordConstant:
            constant = self.expect(self.currentToken()['value'])
            self.VMWriter.writePush(self.keywordConstant[constant], '')

        elif self.currentToken()['value'] == '(':
            self.expect('(')
            self.compileExpression()
            self.expect(')')