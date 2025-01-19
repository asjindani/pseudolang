class Call:
    def __init__(self, method, values, line):
        self.method = method
        self.values = values
        self.line = line
        self.exit = False
    def __repr__(self):
        return f"Call({self.method}, {self.values})"

class IdentifierBased:
    def __init__(self, name, type, data):
        self.name = name
        self.data = data
        self.type = type
    def out(self):
        return self.data
    def __repr__(self):
        return f"{self.__class__.__name__}({self.data})"

class Variable(IdentifierBased):
    def __init__(self, name, type, data = None):
        super().__init__(name, type, data)

class Constant(IdentifierBased):
    def __init__(self, name, type, data):
        super().__init__(name, type, data)

class Method(IdentifierBased):
    def __init__(self, name, statements, line, type_ = None):
        super().__init__(name, type_, statements)
        self.line = line
    def out(self):
        return f"<{self.__class__.__name__.toupper()} '{self.name}'>"

class Function(Method):
    def __init__(self, name, statements, line, type_):
        super().__init__(name, statements, line, type_)

class Procedure(Method):
    def __init__(self, name, statements, line, type_ = None):
        super().__init__(name, statements, line, type_)
        self.statements = statements