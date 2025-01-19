# PseudoLang

A project that aims to make pseudocode more accessible to students.

Inspired by the pseudocode syntax in [A Level Computer Science](https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-international-as-and-a-level-computer-science-9618/).

# How to use?

First, install Python from the official website [Python.org](https://python.org).

Now, open the terminal and naviate to your working directory.

Next, if you have git installed, clone this repository on your system.

```git
git clone https://github.com/asjindani/pseudolang.git
```

If you do not have git on your system, you can download a zip file of the code by going to this page [here](https://github.com/asjindani/pseudolang)), clicking on `Code` button and then the `Download ZIP` option. You can extract the folders into your working directory (see directory structure below).

```
working-directory/
  pseudolang/
    examples/
    modules/
```

Create a new `main.pseudo` file in the working directory.

Type the following code into  the`main.pseudo` file:

```
OUTPUT "Hello world!"
```

Then, type the following command:

```
python -m pseudolang main.pseudo
```

You should see the output:

```
Hello world!
```

To execute the code in developer mode:

```
python -m pseudolang main.pseudo -dev
```

You can also try one of the example codes:
```
python -m pseudolang pseudolang/examples/multiplication.pseudo
```

# Data Types

Following are the supported data types in PseudoLang.

## 1. String

`STRING` is a collection of characters enclosed by double quotes (`"`).

Examples: `"Hello"`, `"Name241"`, `"$$$"`

## 2. Integer

`INTEGER` is a whole number without a decimal point.

Examples: `100`, `0`, `-5`

## 3. Real

`REAL` is a real number with a decimal point.

Examples: `2.5`, `0.0`, `-2.0`

## 4. Character

`CHAR` is a single character enclosed by single quotes (`'`).

Examples: `'a'`, `'5'`, `'%'`

## 5. Boolean

`BOOLEAN` is a binary type which can have one of two possible states.

Examples: `TRUE`, `FALSE`

# Syntax

Following are the supported syntax for PseudoLang.

Angular brackets are used to indicate the syntax.

## Variables

To declare a variable, provide the identifier (name) and data type.

```
DECLARE <identifier> : <data-type>
```

Multiple variables of the same data type can be declared together.

```
DECLARE <identifier1>, <identifier2>, <...> : <data-type>
```

To assign a value to a variable, use the assignment operator (`<-`).

Examples

```
DECLARE Name : STRING
Name <- "ABC"
```

```
DECLARE Age, Marks : INTEGER
Age <- 10
Marks <- 89
```

## Constants

Constants are used for a value that does not change during execution of the program.

Constants can be declared by providing a name (identifier) and a value.

The data type of the constant is determined by the value.

```
CONSTANT <identifier> = <value>
```

Examples

```
CONSTANT Pi = 3.14159265
```

```
CONSTANT Username = "admin"
```

## Input / Output

To get the value of a variable from the user, you can use the `INPUT` statement.

```
INPUT <identifier>
```

To display the result of an expression to the terminal, use the `OUTPUT` statement.

```
OUTPUT <expression>
```

`OUTPUT` statement can contain multiple expressions separated by a comma (`,`).

```
OUTPUT <expression1>, <expression2>, <...>
```

Examples

```
INPUT Name
OUTPUT "Hello ", Name
```

```
INPUT Age
OUTPUT Age + 10
```

```
INPUT Marks
OUTPUT Marks / 100
```

## Count-controlled Loop

`FOR` loop can be defined with a start value and end value (both inclusive).

The step value is optional and set to `1` (ascending) or `-1` (descending) by default.

```
FOR <identifier> <- <start-value> TO <end-value>
  <statement1>
  <statement2>
  <...>
NEXT <identifier>
```

```
FOR <identifier> <- <start-value> TO <end-value> STEP <step-value>
  <statement1>
  <statement2>
  <...>
NEXT <identifier>
```

Example

```
DECLARE Index : INTEGER
FOR Index <- 1 TO 10
  OUTPUT Index
NEXT Index
```

## Pre-condition Loop

`WHILE` loop evaluates the condition first and then executes the code if the condition is `TRUE`. 

The loop is terminated when the condition evaluates to `FALSE`.

```
WHILE <condition>
  <statement1>
  <statement2>
  <...>
ENDWHILE
```

Example

```
DECLARE Index : INTEGER
Index <- 1
WHILE Index < 11
  OUTPUT Index
  Index <- Index + 1
ENDWHILE
```

## Post-condition Loop

`REPEAT` loop executes the statements first and then evaluates the condition.

The loop is terminated when the condition evaluates to `TRUE`.

```
REPEAT
  <statement1>
  <statement2>
  <...>
UNTIL <condition>
```

Example

```
DECLARE Index : INTEGER
Index <- 1
REPEAT
  OUTPUT Index
  Index <- Index + 1
UNTIL Index > 10
```
