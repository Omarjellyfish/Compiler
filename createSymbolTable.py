from SymbolTable import SymbolTableEntry
import copy
import tokenizer

def createSymbolTable(tokens):
    symbolTable = []
    for i in range(len(tokens)):
        if tokens[i][0] == "IDENTIFIER":
            for j in symbolTable:
                if j.name == tokens[i][1]:
                    symbolTable[symbolTable.index(j)].addLine(tokens[i][2])
                    break
            else:
                if len(symbolTable) == 0:
                    address = 0
                else:
                    address = calcAddress(symbolTable[-1])

                tmp = SymbolTableEntry(tokens[i][1], address, 4, 1, tokens[i][2])
                symbolTable.append(tmp)

    return symbolTable


def calcAddress(prevSymbolTableEntry):
    address = prevSymbolTableEntry.address

    address += prevSymbolTableEntry.calculateTotalSize()

    return address

def main():
    tokens = tokenizer.execute()
    print("name\taddress\tdimensions\tline declared\tlines mentioned")
    for i in createSymbolTable(tokens):
        print(i)

if __name__ == "__main__":
    main()