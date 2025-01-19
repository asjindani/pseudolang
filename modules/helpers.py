from termcolor import colored
from .data_types import *

def printc(color, *args, **kwargs):
    if "sep" in kwargs:
        kwargs["sep"] = colored(kwargs["sep"], color)
    if "end" in kwargs:
        kwargs["end"] = colored(kwargs["end"], color)
    print(*(colored(arg, color) for arg in args), **kwargs)

def convert_literal_to_python(value : str):
    if value.startswith("\"") and value.endswith("\""):
        return String(value[1:-1])
    if value.startswith("\'") and value.endswith("\'") and len(value) == 3:
        return Char(value[1:-1])
    if all([i.isdigit() or i == '-' for i in value]) and len(value) > 0:
        return int(value)
    if value == "TRUE":
        return Boolean(True)
    if value == "FALSE":
        return Boolean(False)
    try:
        return float(value)
    except ValueError:
        return None
    

def valid_identifier(identifier : str):
    return len(identifier) > 0 and identifier[0].isalpha() and all([i.isalnum() or i == "_" for i in identifier])


# def convert_literal_to_python_with_errors(value : str, data_type : str):
#     if data_type == "STRING":
#         noerrorif(value.startswith("\"") and value.endswith("\""), "STRING Must Start And End With Double Quotes")
#     if data_type == "CHAR":
#         noerrorif(value.startswith("\'") and value.endswith("\'"), "CHAR Must Start And End With Single Quotes")
#         noerrorif(len(value) == 3, "CHAR Must Have Only One Character")
#     if data_type == "INTEGER":
#         noerrorif(value.isdigit())
#     if data_type == "REAL":
#         try:
#             float(value)
#         except ValueError:
#             noerrorif(False)
#     if data_type == "BOOLEAN":
#         noerrorif(value == "TRUE" or value == "FALSE", "BOOLEAN Value Must Be TRUE or FALSE")
#     return convert_literal_to_python(value)