import re
import json
import cgitb; cgitb.enable()
import cgi

class Parser:

    mainDeclared = False
    varType = []
    varName = []
    varValue = []
    arrayIterator = 0
    lineNumber = 0
    outputFile = 'output.txt'


    def __init__(self, outputFile='output.txt'):
        if not(outputFile is None):
            self.outputFile = outputFile

    def getNextLine(line):

        if mainDeclared == False: #is a main fxn declared?

            mainDeclaration() #if not, look to see if this line declares it

        else:

            searcher(line) #if declared, look to see if anything valuable is on the line

    def mainDeclaration(line):

        if mainDeclared == False: #main fxn has not been called yet

            if re.compile(r'''(
                #(.*)
                ()'static void main') ?
                ''') is None:
                #if main method not declared
                    getNextLine(line)

            else:
            #main has been declared
                mainDeclared = True
                searcher(line)

    def searcher(line):

        if re.compile(r'''(
             (byte|sbyte|int|uint|short|ushort|long|ulong|float|double|char|decimal) #finds type if mainDeclaration
             )''') is None:
             #nothing declared, search to see if a variable changes
                 variableChangeSearch(line)

        else:

            varType = group()

            regexSearch = re.compile(r'''(
                (\w+)   #find variable name
            )''')

            varName[arrayIterator] = group()

            if re.compile(r'''(
                         (=)?    #does the variable have a value declared?
                          )''') is None:

                varValue[arrayIterator] = None
                arrayIterator += 1

                #makeJSON()

            else:

                regexSearch = re.compile(r'''(
                    (\w+)   #find the name
                )''')

                varValue[arrayIterator] = group()
                arrayIterator += 1
                #makeJSON()

    def variableChangeSearch():

        regexSearch = re.compile(r'''(
                                (\w+)   #find the name; group 1
                                (\s*)   #0 or more spaces; group 2
                                (=|\+\+|--) #equals sign, plus plus, or minus minus; group 3
                                (\s*)	#pasrse out the spaces; group 4
                                (\w*)	#any variables used in equation; group 5
                                 )''')


        found = False

        i = 0
        while (i < arrayIterator):

            if (varName[i] == group(1)):

                i = arrayIterator
                found = True

            else:

                i += 1

        if found and (group(5) is None):

            if group(3) == '++':

                if isinstance(varType[arrayIterator], types.StringTypes):

                    varValue[arrayIterator] += 1

        elif group(3) == '--':

            if isinstance(varType[arrayIterator], types.StringTypes):

                varValue[arrayIterator] -= 1

        elif found:

            regexSearch = re.compile(r'''(
                                    ((\w*)
                                      \s*
                                    (\+|-)
                                      \s*)*
                                     )''')

        operators = (len(group(0)) - 1) / 2 #number of operators
        varsUsed = group(1)
        opsUsed = group(2)

        j = 0

        while j < len(varsUsed):

            if isinstance(varsUsed[j], types.StringTypes):

                k = 0

                while k < len(varName):

                    if varName[k] == varsUsed[j]:

                        varsUsed[j] = varValue[k]
                    k += 1
            j += 1

        result = varsUsed[0]

        j = 0

        while j < len(opsUsed):

            if opsUsed[j] == '+':

                result = result + varsUsed[j + 1]

            elif opsUsed[j] == '-':

                result = result - varsUsed[j + 1]

            j += 1

        self.varValue[self.arrayIterator] = result

    def makeJSON():

        data = [lineNumber, varType, varName, varValue]
        with open('output.txt', 'r+') as outputFile:
            json.dump(data, outfile)
        outputFile.close()

        #takes lineNumber, varType array, varName array, and varValue array and puts into JSON format
        #sends JSON to frontend

    def main(self): #iterate through lines of textfile

        p = Parser.parser()
        p.lineNumber = 0
        dataFromJS = cgi.FieldStorage()
        codeLines = dataFromJS.list[0].value.split('\n')
        while (len(codeLines) > 0 and (p.lineNumber <= 300)):
            p.getNextLine(codeLines[0])
            codeLines.pop(0)
            p.lineNumber += 1
