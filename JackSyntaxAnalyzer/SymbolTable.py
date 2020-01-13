
class SymbolTable:

    def __init__(self):
        self.classSymbolTable = {'names' : [], 'type' : [], 'kind' : [], 'position' : []}
        self.classVariableKinds = ['field', 'static']
        self.subroutineVariableKinds = ['local', 'argument']
        self.subroutineTypes = ['method', 'constructor', 'function']

    # resets the subroutine symbol table in preparation to compile a new subroutine
    def startNewSubroutine(self):
        self.subroutineSymbolTable = {'names' : [], 'type' : [], 'kind' : [], 'position' : []}

    # returns the number of local variables in a subroutine
    def getNumberOfLocalVars(self):
        return self.getVariableKindCount(self.subroutineSymbolTable, 'local')

    # returns the number of field variables in a class, for the constructor
    def getNumberOfFieldVars(self):
        return self.getVariableKindCount(self.classSymbolTable, 'field')

    # adds variables to their respective 'scope' {symbol table}
    def addVariable(self, variable):
        scope = dict()

        if variable['kind'] in self.subroutineVariableKinds:
            scope = self.subroutineSymbolTable
        elif variable['kind'] in self.classVariableKinds:
            scope = self.classSymbolTable

        scope['names'].append(variable['name'])
        scope['kind'].append(variable['kind'])
        scope['position'].append(self.getVariableKindCount(scope, variable['kind']) - 1)
        scope['type'].append(variable['type'])

    # returns the count of variables of any kind supplied
    def getVariableKindCount(self, scope, kind):
        count = len([variable for variable in scope['kind'] if variable == kind])
        return count

    # returns the index of the supplied variable in the 'names' key of the symbol table
    def getVariableNameIndex(self, variable):
        variableNameIndex, scope = None, None
        try:
            variableNameIndex = self.subroutineSymbolTable['names'].index(variable)
            scope = self.subroutineSymbolTable
        except:
            try:
                variableNameIndex = self.classSymbolTable['names'].index(variable)
                scope = self.classSymbolTable
            except:
                return variableNameIndex, scope
        return variableNameIndex, scope

    # returns the 'kind' of the variable
    def getVariableKind(self, variable):
        variableIndex, scope = self.getVariableNameIndex(variable)
        if variableIndex is not None:
            segment = scope['kind'][variableIndex]
            if segment == 'field':
                return 'this'
            return segment
        return variableIndex

    # returns the 'type' of the variable
    def getVariableType(self, variable):
        variableIndex, scope = self.getVariableNameIndex(variable)
        if variableIndex is not None:
            return scope['type'][variableIndex]
        return variableIndex

    # returns the 'type' of the variable
    def getVariablePosition(self, variable):
        variableIndex, scope = self.getVariableNameIndex(variable)
        if variableIndex is not None:
            return scope['position'][variableIndex]
        return variableIndex