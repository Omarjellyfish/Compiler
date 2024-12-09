class SymbolTableEntry:
    lines_mentioned = set()

    def __init__(self, name, address, size, dim, line_declared):
        self.name = name
        self.address = address
        self.size = size
        self.dim = dim
        self.line_declared = line_declared
        self.lines_mentioned = set()

    def addLine(self, lineNum):
        self.lines_mentioned.add(lineNum)

    def calculateTotalSize(self):
        return (self.size * self.dim)
    
    def __repr__(self):
        return (f"{self.name}\t{self.address}\t{self.dim}\t\t{self.line_declared}\t\t{self.lines_mentioned}")