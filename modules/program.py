import re

from termcolor import cprint

from .data_types import *
from .opcodes import *
from .classes import *
from .helpers import *
from .errors import *
from .regex import *

class Program:
    def __init__(self, lines, dev = False):
        self.line = 1
        self.lines = lines
        self.dev = dev
        self.block = 0
        self.instructions = None
        self.call_stack = None

    def new_call(self, call : Call):
        try:
            self.call_stack.push(call)
        except AssertionError:
            self.throw(Error, "Call stack has reached maximum capacity", "Stack Overflow Error")

    @property
    def var(self):
        return self.call_stack.top.values

    def run(self, dev: None = None):
        if self.instructions is None:
            self.instructions = self.parse()

        if dev is not None:
            self.dev = dev

        self.call_stack = Stack(256)
        self.new_call(Call(Procedure("MAIN", self.instructions, 1), {}, 1))

        self.line = 1
        self.block = 0

        while self.block < len(self.instructions):
            self.execute(self.instructions[self.block])
            self.line += 1
            self.block += 1

    def count_lines(self, instruction):
        instruction_type = type(instruction)

        if hasattr(instruction, "statements"):
            lines = 2
            if instruction_type == IF:
                lines += len(instruction.conditions)-1
                for statement in instruction.statements:
                    for statement2 in statement:
                        lines += self.count_lines(statement2)
            else:
                for statement in instruction.statements:
                    lines += self.count_lines(statement)
            return lines
        else:
            return 1

    def global_values(self):
        return dict(((key, self.call_stack[0].values[key].data) for key in self.call_stack[0].values))

    def local_values(self):
        return dict(((key, self.var[key].data) for key in self.var))
    
    def scope_values(self):
        values = {}
        for i in range(self.call_stack.pointer+1):
            values = values | dict(((key, self.call_stack[i].values[key].data) for key in self.call_stack[i].values))
        return values
    
    def evaluate(self, expression : str):
        if type(expression) in PYTHON_TO_PSEUDO:
            return expression
        literal = convert_literal_to_python(expression)
        if literal is not None:
            return literal

        global_ = self.global_values()
        scope = self.scope_values()
        
        try:
            return eval(expression, global_, scope)
        except NameError as e:
            identifier = str(e).split("'")[1]
            self.throw(Error, f"Invalid identifier '{identifier}'", "Name Error")
        except Exception as e:
            cprint(f"{e.__class__.__name__}: {e}", "red")
        
        # if expression in var:
        #     value = var[expression].data
        #     noerrorif(value is not None, "Value Not Initialized")
        #     return value
        
    def get_properties(self, identifier):
        if identifier in self.var:
            return self.var[identifier]
        elif identifier in self.call_stack[0].values:
            return self.call_stack[0].values[identifier]

    def identifier_present(self, identifier):
        return identifier in self.var or identifier in self.call_stack[0].values

    def assign(self, identifier, expression : str):

        if not self.identifier_present(identifier):
            self.throw(NoDeclarationError, identifier)

        if identifier in KEYWORDS:
            self.throw(Error, f"{identifier} is a keyword", "Name Error")

        properties = self.get_properties(identifier)

        if type(properties) == Constant:
            self.throw(Error, f"Value cannot be reassigned to constant '{identifier}'")

        value = self.evaluate(expression)

        if value is None:
            self.throw(Error, "Invalid Expression, " + expression)

        value_data_type = PYTHON_TO_PSEUDO[type(value)]
        data_type = properties.type

        if data_type != value_data_type:
            self.throw(Error, f"Data Type Mismatch: {data_type} <- {value_data_type}")
        
        properties.data = value

        if self.dev:
            cprint(f"{identifier} has been assigned value {value}", "blue")

    def declare_variables(self, identifiers, data_type):
        if data_type not in DATA_TYPES:
            self.throw(Error, "Invalid Data Type", "Type Error")
        for identifier in identifiers:
            if identifier in KEYWORDS:
                self.throw(Error, f"{identifier} is a keyword", "Name Error")
            if identifier in self.var:
                self.throw(ReDeclarationError, identifier)
            if not valid_identifier(identifier):
                self.throw(Error, "Invalid Identifier", "Name Error")
                
            self.var[identifier] = Variable(identifier, data_type)

        if self.dev:
            if len(identifiers) == 0:
                return
            if len(identifiers) == 1:
                cprint(f"Declared variable '{identifiers[0]}' with type {data_type}", "blue")
            else:
                cprint(f"Declared variables {identifiers.__repr__()[1:-1]} with type {data_type}", "blue")

    def declare_constant(self, identifier, expression):
        value = self.evaluate(expression)
        if value is None:
            self.throw(Error, "Invalid Expression")
        if identifier in self.var:
            self.throw(ReDeclarationError, identifier)
        if identifier in KEYWORDS:
            self.throw(Error, f"{identifier} is a keyword", "Name Error")
        if not valid_identifier(identifier):
            self.throw(Error, "Invalid Identifier", "Name Error")
        data_type = PYTHON_TO_PSEUDO[type(value)]
        self.var[identifier] = Constant(identifier, data_type, value)

        if self.dev:
            cprint(f"Declared constant '{identifier}' with type {data_type} and value {value}", "blue")

    def declare_method(self, instruction):
        identifier = instruction.identifier
        parameters = instruction.parameters
        statements = instruction.statements

        if self.dev:
            for index in range(self.count_lines(instruction)-1):
                cprint(self.lines[self.line + index], "magenta")

        if identifier in self.var:
            self.throw(Error, f"Identifier '{identifier}' is already used", "Name Error")

        if hasattr(instruction, "return_type"):
            return_type = instruction.return_type
            self.var[identifier] = Function(identifier, instruction, self.line, return_type)
        else:
            self.var[identifier] = Procedure(identifier, instruction, self.line)

        # self.line += len(instruction.statements) + 1 # +1 for ENDPROCEDURE
        self.line += self.count_lines(instruction)-1
        
        if self.dev:
            cprint(f"Procedure '{identifier}' has been created", "blue")

    def parse_method(self, string):
        # Name()
        # Name(x1 : INTEGER)
        # Name(x1 : INTEGER, y2 : STRING)
        match1 = re.match(METHOD_DECLARATION_1, string)

        # Name(x1, y1 : INTEGER)
        # Name(x1, y1, z1 : INTEGER)
        match2 = re.match(METHOD_DECLARATION_2, string)

        if match1 is None and match2 is None:
            self.throw(Error, "Invalid Header", "Syntax Error")

        if match1:
            string = match1.group(2)
            parameters = []
            data_types = []
            declarations = []

            if string is not None:
                pairs = string.split(",")

                for pair in pairs:
                    pair_split = pair.split(":")
                    identifier = pair_split[0].strip()
                    data_type = pair_split[1].strip()
                    parameters.append(identifier)
                    data_types.append(data_type)
                    declarations.append(DECLARE((identifier,), data_type))
                
            identifier = match1.group(1).strip()

        elif match2:

            parameters = [var.strip() for var in match2.group(2).split(",")]

            data_types = [match2.group(3).strip() for _ in range(len(parameters))]

            identifier = match2.group(1).strip()
            declarations = (DECLARE(parameters, data_type),)
        
        return identifier, parameters, data_types


    def parse(self):

        self.line = 1

        stack = Stack(256)
        stack.push([])

        stack2 = Stack(256)

        for file_line in self.lines:
            instructions = stack.top
            parts = file_line.split()

            # Blank Line
            if not parts:
                self.line += 1
                instructions.append(tuple())
                continue

            if len(parts) > 1 and parts[1] == "<-":
                opcode = "ASSIGNMENT"
            else:
                opcode = parts[0]

            if opcode == "DECLARE":
                value = " ".join(parts[1:])
                value_split = [i.strip() for i in value.split(":")]
                if len(value_split) != 2:
                    self.throw(Error, "Invalid Syntax: Must Use One Colon")

                identifiers = tuple(i.strip() for i in value_split[0].split(","))
                data_type = value_split[1]

                instructions.append(DECLARE(identifiers, data_type))

            elif opcode == "CONSTANT":
                value_split = " ".join(parts[1:]).split("=")
                identifier = value_split[0].strip()
                value = value_split[1].strip()
                instructions.append(CONSTANT(identifier, value))

            elif opcode.startswith("//"):
                value = " ".join(parts[1:])
                instructions.append(COMMENT(value))

            elif opcode == "ASSIGNMENT":
                identifier = parts[0]
                value = " ".join(parts[2:])
                instructions.append(ASSIGNMENT(identifier, value))

            elif opcode == "INPUT":
                if len(parts) < 2:
                    self.throw(Error, "Input identifier is missing", "Parse Error")
                identifier = parts[1]
                instructions.append(INPUT(identifier))

            elif opcode == "OUTPUT":
                values = " ".join(parts[1:]).split(",")
                values = [i.strip() for i in values]
                instructions.append(OUTPUT(values))

            elif opcode == "IF":
                if parts[-1] != "THEN":
                    self.throw(Error, "THEN missing after IF")
                condition = " ".join(parts[1:-1])
                instructions.append(IF([condition], [[]]))
                stack.push(instructions[-1][-1][-1])
                stack2.push((self.line, instructions[-1]))

            elif opcode == "ELSE":
                if not(len(parts) == 1 or parts[1] == "IF"):
                    self.throw()
                stack.pop()
                instructions = stack.top
                if len(parts) > 1 and parts[1] == "IF":
                    if parts[-1] != "THEN":
                        self.throw(Error, "THEN missing after IF")
                    condition = " ".join(parts[2:-1])
                else:
                    condition = "ELSE"
                instructions[-1][0].append(condition)
                instructions[-1][1].append([])
                stack.push(instructions[-1][-1][-1])
                stack2.push((self.line, instructions[-1]))

            elif opcode == "ENDIF":
                stack.pop()
                stack2.pop()

                instructions = stack.top

                if instructions is None or type(instructions[-1]) != IF:
                    self.throw(Error, "ENDIF must be used after IF")

            elif opcode == "FOR":
                if parts[2] != "<-":
                    self.throw()
                if parts[4] != "TO":
                    self.throw()
                if not(len(parts) == 6 or parts[6] == "STEP"):
                    self.throw()

                identifier = parts[1]
                lower = parts[3]
                upper = parts[5]
                step = parts[7] if len(parts) > 6 else "1" if upper >= lower else "-1"

                instructions.append(FOR(identifier, lower, upper, step, []))
                stack.push(instructions[-1][-1])
                stack2.push((self.line, instructions[-1]))

            elif opcode == "NEXT":
                identifier = parts[1]

                stack.pop()
                stack2.pop()

                instructions = stack.top

                if instructions is None or type(instructions[-1]) != FOR:
                    self.throw(Error, "NEXT Must Be Used After FOR")
                if instructions[-1].identifier != identifier:
                    self.throw(Error, f"Identifier Mismatch: {instructions[-1].identifier} vs {identifier}")

            elif opcode == "WHILE":
                condition = " ".join(parts[1:])
                instructions.append(WHILE(condition, []))
                stack.push(instructions[-1][-1])
                stack2.push((self.line, instructions[-1]))

            elif opcode == "ENDWHILE":
                stack.pop()
                stack2.pop()

                instructions = stack.top

                if instructions is None or type(instructions[-1]) != WHILE:
                    self.throw(Error, "ENDWHILE must be used after WHILE")

            elif opcode == "REPEAT":
                instructions.append(REPEAT([], ""))
                stack.push(instructions[-1].statements)
                stack2.push((self.line, instructions[-1]))

            elif opcode == "UNTIL":
                stack.pop()
                stack2.pop()

                instructions = stack.top

                if instructions is None or type(instructions[-1]) != REPEAT:
                    self.throw(Error, "UNTIL must be used after REPEAT")

                condition = " ".join(parts[1:])
                instructions[-1] = REPEAT(instructions[-1][0], condition)

            elif opcode == "PROCEDURE":
                string = " ".join(parts[1:])
                identifier, parameters, data_types = self.parse_method(string)
                instructions.append(PROCEDURE(identifier, parameters, data_types, []))
                stack.push(instructions[-1].statements)
                stack2.push((self.line, instructions[-1]))

            elif opcode == "ENDPROCEDURE":
                stack.pop()
                stack2.pop()

                instructions = stack.top

                if instructions is None or type(instructions[-1]) != PROCEDURE:
                    self.throw(Error, "ENDPROCEDURE cannot be used without PROCEDURE")

            elif opcode == "CALL":
                string = " ".join(parts[1:])
                regex1 = r"^(\w+)\s*\(((?:[^,]+,)*(?:[^,]+)?)\)$"
                
                match1 = re.match(regex1, string)

                if match1 is not None:
                    identifier = match1.group(1).strip()
                    arguments = [a.strip() for a in match1.group(2).split(",")]
                    instructions.append(CALL(identifier, arguments))
                else:
                    self.throw(Error, "Invalid CALL Syntax", "Syntax Error")
                
            elif opcode == "FUNCTION":
                return_type = parts[-1]

                if return_type not in DATA_TYPES:
                    self.throw(Error, "Invalid data type", "Type Error")
                if parts[-2] != "RETURNS":
                    self.throw(Error, "RETURNS is missing", "Syntax Error")

                string = " ".join(parts[1:-2])
                identifier, parameters, data_types = self.parse_method(string)
                instructions.append(FUNCTION(identifier, parameters, data_types, return_type, []))
                stack.push(instructions[-1].statements)
                stack2.push((self.line, instructions[-1]))

                print(string)
            
            elif opcode == "ENDFUNCTION":
                stack.pop()
                stack2.pop()

                instructions = stack.top

                if instructions is None or type(instructions[-1]) != FUNCTION:
                    self.throw(Error, "ENDFUNCTION cannot be used without FUNCTION", "Block Error")

            elif opcode == "RETURN":
                expression = " ".join(parts[1:])
                instructions.append(RETURN(expression))

            else:
                instructions.append(UNKNOWN(file_line))
                # self.throw(ParseError, "Unknown Opcode")

            self.line += 1

            if self.dev:
                cprint(instructions[-1], "green")

        if len(stack) > 1:
            self.line = stack2.top[0]
            instruction = stack2.top[1]
            self.throw(ParseError, f"{instruction.__class__.__name__} block was not closed")

        self.instructions = stack.top
        return stack.top
    
    def execute(self, instruction):

        if self.dev:
            print()
            cprint(f"Block {self.block+1} • Line {self.line}", "yellow")
            if len(self.call_stack) > 1:
                cprint(tuple(i.method.name for i in self.call_stack), "yellow")
            if self.lines[self.line-1]:
                cprint(self.lines[self.line-1], "magenta")
            if instruction:
                cprint(instruction, "green")

        # Blank Line
        if not instruction:
            return

        instruction_type = type(instruction)

        if instruction_type == DECLARE:
            identifiers = instruction.identifiers
            data_type = instruction.data_type

            self.declare_variables(identifiers, data_type)

        elif instruction_type == CONSTANT:
            identifier = instruction.identifier
            expression = instruction.value
            self.declare_constant(identifier, expression)

        elif instruction_type == ASSIGNMENT:
            identifier = instruction.identifier
            value = instruction.value
            self.assign(identifier, value)

        elif instruction_type == INPUT:
            identifier = instruction.identifier
            if identifier not in self.var:
                self.throw(NoDeclarationError, identifier)
            python_type = PSEUDO_TO_PYTHON[self.var[identifier].type]

            value = None
            while value is None:
                try:
                    value = python_type(input())
                except:
                    value = None

            variable = self.var[identifier]
            variable.data = value

        elif instruction_type == OUTPUT:
            expressions = instruction[0]
            for expression in expressions:
                if expression:
                    result = self.evaluate(expression)
                    if result is None:
                        self.throw(Error, f"Cannot evaluate the expression, {expression}")
                    print(result, end="")
                else:
                    self.throw(Error, "Output expression is missing")
            print()

        elif instruction_type == IF:
            index = 0
            net_result = False
            while index < len(instruction.conditions):
                condition = instruction.conditions[index]
                if condition == "ELSE":
                    result = True
                else:
                    result = self.evaluate(condition)
                    if result is None:
                        self.throw(Error, "Invalid Condition")
                
                result = (not net_result) and (result == TRUE)
                statements = instruction.statements[index]
                if len(statements) == 0:
                    self.throw(Error, "No Statements Inside Block")
                for statement in statements:
                    if self.call_stack.top.exit:
                        self.call_stack.top.exit = False
                        break
                    self.line += 1
                    if result == TRUE:
                        self.execute(statement)
                net_result = net_result or (result == TRUE)
                index += 1
                self.line += 1

        elif instruction_type == FOR:
            identifier = instruction.identifier
            lower = self.evaluate(instruction.lower)
            upper = self.evaluate(instruction.upper)
            step = self.evaluate(instruction.step)
            statements = instruction.statements

            if lower is None:
                self.throw(Error, "Invalid lower bound")
            if upper is None:
                self.throw(Error, "Invalid upper bound")
            if step is None:
                self.throw(Error, "Invalid step")

            if upper >= lower:
                upper += 1
            else:
                upper -= 1

            for index in range(lower, upper, step):
                self.assign(identifier, str(index))
                self.execute_statements(statements)
            self.line += self.count_lines(instruction)-1

        elif instruction_type == WHILE:
            condition = instruction.condition
            statements = instruction.statements

            result = self.evaluate(condition)

            line_old = self.line
            while result == TRUE:
                self.execute_statements(statements)
                result = self.evaluate(condition)
                if result is None:
                    self.throw(Error, "Condition could not be evaluated")
            self.line += self.count_lines(instruction)-1

        elif instruction_type == REPEAT:
            condition = instruction.condition
            statements = instruction.statements

            result = FALSE

            while result == FALSE:
                self.execute_statements(statements)
                result = self.evaluate(condition)
                line_old = self.line
                self.line += self.count_lines(instruction)-1
                if result is None:
                    self.throw(Error, "Condition could not be evaluated")
                self.line = line_old
            self.line += self.count_lines(instruction)-1

        elif instruction_type == PROCEDURE or instruction_type == FUNCTION:
            self.declare_method(instruction)

        elif instruction_type == CALL:
            identifier = instruction.identifier
            arguments = instruction.arguments

            if not self.identifier_present(identifier):
                self.throw(Error, f"Unknown identifier '{identifier}'")

            procedure = self.get_properties(identifier)

            if type(procedure) != Procedure:
                self.throw(Error, f"CALL cannot be used with {PYTHON_TO_PSEUDO[procedure.data.__class__]} '{identifier}'", "Syntax Error")

            instruction = procedure.statements

            parameters = instruction.parameters
            data_types = instruction.data_types

            statements = instruction.statements

            if len(parameters) != len(arguments):
                self.throw(Error, "Number of arguments must match number of parameters", "Temp Error")

            call = Call(procedure, {}, self.line)
            self.new_call(call)

            for index in range(len(parameters)):
                self.declare_variables((parameters[index],), data_types[index])
                self.call_stack.pop()
                value = self.evaluate(arguments[index])
                self.new_call(call)
                self.assign(parameters[index], value)

            if self.dev:
                cprint(f"Global: {dict((k,v) for (k,v) in self.global_values().items() if type(v) != PROCEDURE)}", "blue")
                cprint(f"Local: {dict((k,v) for (k,v) in self.local_values().items() if type(v) != PROCEDURE)}", "blue")
                cprint(f"Scope: {dict((k,v) for (k,v) in self.scope_values().items() if type(v) != PROCEDURE)}", "blue")

            line_old = self.line
            self.line = procedure.line
            for statement in statements:
                if self.call_stack.top.exit:
                    self.call_stack.top.exit = False
                    break
                self.line += 1
                self.execute(statement)
            self.call_stack.pop()
            self.line = line_old
        
        elif instruction_type == RETURN:
            expression = instruction.expression
            self.call_stack.top.exit = True

            if self.dev:
                cprint("Returned to previous scope", "blue")

    def execute_statements(self, statements):
        line_old = self.line
        for statement in statements:
            if self.call_stack.top.exit:
                self.call_stack.top.exit = False
                break
            self.line += 1
            self.execute(statement)
        self.line = line_old

    def throw(self, error_type = Error, *args):

        if self.call_stack:
            print()
            for call in self.call_stack:
                cprint(f"Line {call.line} calls {call.method.name}", "yellow")
                cprint(f"\tProgram Code:\t{self.lines[call.line-1]}", "yellow")

        error_type(*args).throw(self.line, self.lines[self.line-1])

        # print([[j for j in i.values] for i in self.call_stack])

        if self.dev:
            print()
            raise AssertionError()
        exit()