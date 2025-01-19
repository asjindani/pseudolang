from collections import namedtuple

KEYWORDS = [
    "DECLARE",
    "CONSTANT",
    "INPUT",
    "OUTPUT",
    "IF",
    "FOR",
    "TO",
    "STEP",
    "NEXT",
    "WHILE",
    "ENDWHILE",
    "REPEAT",
    "UNTIL",
    "PROCEDURE",
    "ENDPROCEDURE",
    "CALL",
]

DECLARE = namedtuple("DECLARE", "identifiers data_type")
CONSTANT = namedtuple("CONSTANT", "identifier value")
COMMENT = namedtuple("COMMENT", "value")
ASSIGNMENT = namedtuple("ASSIGNMENT", "identifier value")
INPUT = namedtuple("INPUT", "identifier")
OUTPUT = namedtuple("OUTPUT", "exp")
IF = namedtuple("IF", "conditions statements")
FOR = namedtuple("FOR", "identifier lower upper step statements")
WHILE = namedtuple("WHILE", "condition statements")
REPEAT = namedtuple("REPEAT", "statements condition")
PROCEDURE = namedtuple("PROCEDURE", "identifier parameters data_types statements")
CALL = namedtuple("CALL", "identifier arguments")
FUNCTION = namedtuple("FUNCTION", "identifier parameters data_types return_type statements")
RETURN = namedtuple("RETURN", "expression")
UNKNOWN = namedtuple("UNKNOWN", "expression")