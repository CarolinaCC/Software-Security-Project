# About

This project aims at building a static analysis tool for detecting common vulnerabilities in web applications, mainly SQL Injection, XSS Injection, Command Injection and Path Traversal.

The tool is based on techniques described on papers that can be found in the readings folder.

It takes as input an AST (Abstract Syntax Tree) file of a certain python project and a vulnerable patterns file and produces a file containing a list of patterns found in in python project

A complementary report of the tool developed is avaliable in the report folder

Example inputs are given in the examples folder. To run all the examples use the run script provided.

Your program takes two arguments:

the name of the JSON file containing the program slice to analyse, represented in the form of an Abstract Syntax Tree (```program.json```);
the name of the JSON file containing the list of vulnerability patterns to consider (```patterns.json```)

To run the program use:

```
python source/main.py program.json patterns.json
```

The result will be stored in a file called ```program.output.json```

Optional parameters (after both files have been specified):

```print``` to print the result to the command line as well as to the output file

```advanced``` the program will try to understand the values of conditions and use it to avoid false positives

```debug``` the prints exta information, like if the information flow is implicit or explicit, and the line and collumns where the source, sink and sanitization happens

## Group 3

### Group members

Carolina Carreira 87641

Miguel Barros 87691

Rafael Branco 87698
