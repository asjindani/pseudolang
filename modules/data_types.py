from .opcodes import *

DATA_TYPES = {"STRING", "INTEGER", "CHAR", "REAL", "BOOLEAN"}# , "DATE"}

class Char:
    def __init__(self, value : str):
        assert len(value) == 1
        self.__value = value
    def __repr__(self):
        return "Char\'" + self.__value + "\'"
    def __str__(self):
        return self.__value
    
class String:
    def __init__(self, value : str):
        self.__value = value
    def __repr__(self):
        return "String\"" + self.__value + "\""
    def __str__(self):
        return self.__value

class Stack:
    def __init__(self, size):
        self.size = size
        self.items = [None for _ in range(size)]
        self.pointer = -1
    def push(self, item):
        assert self.pointer < self.size - 1, "Stack Overflow Error"
        self.pointer += 1
        self.items[self.pointer] = item
    def pop(self):
        if len(self) > 0:
            item = self.top
            self.pointer -= 1
            return item
        else:
            print("Stack Empty")
    @property
    def top(self):
        if len(self) > 0:
            return self.items[self.pointer]
        else:
            print("Stack Empty")
    @top.setter
    def top(self, value):
        if len(self) > 0:  
            self.items[self.pointer] = value
        else:
            print("Stack Empty")
    def __len__(self):
        return self.pointer + 1
    def __repr__(self):
        return f"Stack{tuple(self.items[i] for i in range(self.pointer+1))}"
    def __getitem__(self, index):
        return self.items[index]
    def __iter__(self):
        return iter(self.items[:self.pointer+1])
    
class Boolean:
    def __init__(self, value):
        assert value in {True, False}
        self.value = value
    def __repr__(self):
        if self.value:
            return "TRUE"
        return "FALSE"
    def __bool__(self):
        return self.value
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        if isinstance(other, bool):
            return self.value == other
        return False

TRUE = Boolean(True)
FALSE = Boolean(False)

PSEUDO_TO_PYTHON = {
    "INTEGER" : int,
    "STRING" : String,
    "CHAR" : Char,
    "REAL" : float,
    "BOOLEAN" : Boolean,
    "FUNCTION": FUNCTION,
    "PROCEDURE": PROCEDURE,
}

PYTHON_TO_PSEUDO = dict((v, k) for (k, v) in PSEUDO_TO_PYTHON.items())