from termcolor import colored

class Error:
    def __init__(self, text : str = "", type = ""):
        self.type = None
        self.text = text
        self.type = type
    def throw(self, line : int = None, code : str = ""):
        print()
        print(colored("PSEUDOLANG ERROR", "red"), end="")
        if line:
            print(colored(f" (Line {line})", "red"), end="")
        print()
        if self.type:
            print(colored("\tError Type:\t" + self.type, "red"))
        if code:
            print(colored("\tProgram Code:\t" + code, "red"))
        if self.text:
            print(colored("\tError Message:\t" + self.text, "red"))

class NoDeclarationError(Error):
    def __init__(self, identifier : str):
        super().__init__("You did not declare the variable " + identifier, "Declaration Error")

class ReDeclarationError(Error):
    def __init__(self, identifier : str):
        super().__init__("You have already declared " + identifier, "Declaration Error")

class ParseError(Error):
    def __init__(self, text = ""):
        super().__init__(text, "Parse Error")